#!/usr/bin/env python3
"""Extract the CC0 brain GLB's triangle geometry using only the standard library."""

import argparse
import json
import math
from pathlib import Path
import struct


def read_glb(path):
    data = path.read_bytes()
    if len(data) < 20 or struct.unpack_from("<4sII", data) != (b"glTF", 2, len(data)):
        raise ValueError("Expected a complete glTF 2.0 binary file")
    chunks = []
    offset = 12
    while offset < len(data):
        if offset + 8 > len(data):
            raise ValueError("Truncated GLB chunk header")
        size, kind = struct.unpack_from("<II", data, offset)
        offset += 8
        if size % 4 or offset + size > len(data):
            raise ValueError("Invalid GLB chunk length")
        chunks.append((kind, data[offset:offset + size]))
        offset += size
    if [kind for kind, _ in chunks] != [0x4E4F534A, 0x004E4942]:
        raise ValueError("Expected one JSON chunk followed by one binary chunk")
    document = json.loads(chunks[0][1])
    binary = chunks[1][1]
    buffers = document.get("buffers", [])
    if len(buffers) != 1 or "uri" in buffers[0]:
        raise ValueError("External buffers are not supported")
    if not 0 <= len(binary) - buffers[0]["byteLength"] <= 3:
        raise ValueError("Binary chunk does not match the declared buffer length")
    return document, binary[:buffers[0]["byteLength"]]


def read_accessor(document, binary, index, expected_type, allowed_components):
    accessor = document["accessors"][index]
    component = accessor["componentType"]
    if accessor["type"] != expected_type or component not in allowed_components:
        raise ValueError("Unsupported accessor type")
    if "sparse" in accessor or accessor.get("normalized"):
        raise ValueError("Sparse and normalized accessors are not supported")
    view = document["bufferViews"][accessor["bufferView"]]
    if view.get("buffer", 0) != 0:
        raise ValueError("Only the embedded binary buffer is supported")
    width = {"SCALAR": 1, "VEC3": 3}[expected_type]
    fmt = "<" + {5121: "B", 5123: "H", 5125: "I", 5126: "f"}[component] * width
    size = struct.calcsize(fmt)
    stride = view.get("byteStride", size)
    count = accessor["count"]
    view_start = view.get("byteOffset", 0)
    start = view_start + accessor.get("byteOffset", 0)
    end = start + (count - 1) * stride + size
    view_end = view_start + view["byteLength"]
    if count < 1 or stride < size or not 0 <= view_start <= start < end <= view_end <= len(binary):
        raise ValueError("Accessor lies outside its buffer view")
    return [struct.unpack_from(fmt, binary, start + i * stride) for i in range(count)]


def convert(path):
    document, binary = read_glb(path)
    if any(key in node for node in document.get("nodes", [])
           for key in ("matrix", "translation", "rotation", "scale", "skin")):
        raise ValueError("Transformed or skinned nodes are not supported")
    parts = []
    for mesh in document["meshes"]:
        if len(mesh["primitives"]) != 1:
            raise ValueError("Expected one primitive per anatomical part")
        primitive = mesh["primitives"][0]
        if primitive.get("mode", 4) != 4 or primitive.get("targets"):
            raise ValueError("Only static triangle primitives are supported")
        vertices = read_accessor(document, binary, primitive["attributes"]["POSITION"], "VEC3", {5126})
        indices = [row[0] for row in read_accessor(document, binary, primitive["indices"], "SCALAR", {5121, 5123, 5125})]
        if len(indices) % 3 or max(indices) >= len(vertices):
            raise ValueError("Invalid triangle indices")
        if not all(math.isfinite(value) for vertex in vertices for value in vertex):
            raise ValueError("Non-finite vertex position")
        positions = [round(value, 3) for x, y, z in vertices
                     for value in (x * 1000, (y - 0.063822) * 1000, z * 1000)]
        parts.append({"name": mesh["name"], "positions": positions, "indices": indices})
    if not parts:
        raise ValueError("No anatomical meshes found")
    return {"parts": parts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Downloaded Innerscene brain.glb")
    parser.add_argument("output", type=Path, nargs="?", default=Path(__file__).parent.joinpath("anatomy", "brain-mesh.json"))
    args = parser.parse_args()
    try:
        result = convert(args.input)
    except (OSError, ValueError, KeyError, IndexError, TypeError, struct.error) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"Wrote {len(result['parts'])} anatomical parts to {args.output}")


if __name__ == "__main__":
    main()
