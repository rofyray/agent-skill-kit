"""Exercise documented media recipes on synthetic assets, never external media."""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT/"skills"/"build-cinematic-sites"/"references"/"media-processing.md"


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg and FFprobe are optional")
class CinematicMediaRecipesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        encoders = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, check=True
        ).stdout
        if "libx264" not in encoders:
            raise unittest.SkipTest("The optional recipes require libx264")
        cls.commands = [
            shlex.split(line)
            for block in re.findall(r"```text\n(.*?)\n```", REFERENCE.read_text(encoding="utf-8"), re.S)
            for line in block.splitlines()
            if line.startswith(("ffmpeg ", "ffprobe "))
        ]

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def run_command(self, command: list[str]) -> bytes:
        result = subprocess.run(command, cwd=self.directory, capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8", errors="replace")[-4000:])
        return result.stdout

    def recipe(self, output: str) -> list[str]:
        return next(command.copy() for command in self.commands if command[-1] == output)

    def synthetic(self, name: str, size: str, rate: int, seconds: float, audio: bool = False) -> None:
        command = ["ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i", f"testsrc2=size={size}:rate={rate}"]
        if audio:
            command.extend(["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000"])
        command.extend(["-t", str(seconds), "-c:v", "libx264", "-pix_fmt", "yuv420p"])
        if audio:
            command.extend(["-c:a", "aac"])
        command.append(name)
        self.run_command(command)

    def probe(self, name: str) -> dict:
        return json.loads(self.run_command([
            "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", name
        ]))

    def test_encode_removes_audio_and_bounds_keyframe_distance(self) -> None:
        self.synthetic("raw.mp4", "64x48", 24, 1.5, audio=True)
        self.run_command(self.commands[0])
        self.run_command(self.recipe("hero-scrub.mp4"))
        info = self.probe("hero-scrub.mp4")
        self.assertEqual([stream["codec_type"] for stream in info["streams"]], ["video"])
        video = info["streams"][0]
        self.assertEqual((video["width"], video["height"]), (64, 48))
        self.assertEqual(video["r_frame_rate"], "30/1")
        self.assertEqual(video["pix_fmt"], "yuv420p")
        frames = json.loads(self.run_command([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_frames",
            "-show_entries", "frame=key_frame", "-of", "json", "hero-scrub.mp4"
        ]))["frames"]
        keys = [index for index, frame in enumerate(frames) if frame["key_frame"]]
        self.assertEqual(keys[0], 0)
        self.assertTrue(all(right - left <= 8 for left, right in zip(keys, keys[1:])))
        self.assertLessEqual(len(frames) - keys[-1], 8)
        self.run_command(self.recipe("-"))
        accepted = self.directory/"hero-scrub.mp4"
        accepted.write_bytes(b"accepted-output-must-survive")
        subprocess.run(self.recipe("hero-scrub.mp4"), cwd=self.directory, capture_output=True, timeout=120)
        self.assertEqual(accepted.read_bytes(), b"accepted-output-must-survive")

    def test_extracted_tail_matches_final_decoded_frame(self) -> None:
        self.synthetic("raw.mp4", "64x48", 24, 3)
        self.run_command(self.recipe("last-frame.png"))
        self.run_command(self.recipe("review-middle.png"))
        decoded = self.run_command([
            "ffmpeg", "-v", "error", "-i", "raw.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        tail = self.run_command([
            "ffmpeg", "-v", "error", "-i", "last-frame.png", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ])
        frame_bytes = 64 * 48 * 3
        self.assertEqual(len(tail), frame_bytes)
        self.assertEqual(tail, decoded[-frame_bytes:])
        self.assertNotEqual(tail, decoded[:frame_bytes], "Fixture must distinguish first and last frames")
        self.run_command(self.recipe("hero-scrub.mp4"))
        self.run_command(self.recipe("hero-poster.png"))
        self.assertEqual(self.probe("hero-poster.png")["streams"][0]["width"], 64)

    def test_join_normalizes_mismatched_inputs_and_decodes(self) -> None:
        self.synthetic("segment-a.mp4", "64x48", 24, 0.5)
        self.synthetic("segment-b.mp4", "96x64", 30, 0.6)
        self.run_command(self.recipe("hero-joined.mp4"))
        info = self.probe("hero-joined.mp4")
        video = info["streams"][0]
        self.assertEqual((video["width"], video["height"]), (1920, 1080))
        self.assertEqual(video["r_frame_rate"], "30/1")
        self.assertAlmostEqual(float(info["format"]["duration"]), 1.1, delta=0.04)
        self.run_command(["ffmpeg", "-v", "error", "-i", "hero-joined.mp4", "-f", "null", "-"])

    def test_documented_dissolve_uses_actual_overlap(self) -> None:
        self.synthetic("segment-a.mp4", "64x48", 30, 6)
        self.synthetic("segment-b.mp4", "96x64", 30, 1)
        command = self.recipe("hero-joined.mp4")
        filter_index = command.index("-filter_complex") + 1
        command[filter_index] = command[filter_index].replace(
            "concat=n=2:v=1:a=0", "xfade=transition=fade:duration=0.25:offset=5.75"
        )
        self.run_command(command)
        duration = float(self.probe("hero-joined.mp4")["format"]["duration"])
        self.assertAlmostEqual(duration, 6.75, delta=0.05)
        self.run_command(["ffmpeg", "-v", "error", "-i", "hero-joined.mp4", "-f", "null", "-"])

    def test_still_derivative_keeps_aspect(self) -> None:
        self.run_command([
            "ffmpeg", "-v", "error", "-n", "-f", "lavfi", "-i", "testsrc2=size=1920x1080",
            "-frames:v", "1", "-update", "1", "photo-source.png"
        ])
        self.run_command(self.recipe("photo-web.jpg"))
        image = self.probe("photo-web.jpg")["streams"][0]
        self.assertEqual((image["width"], image["height"]), (1600, 900))


if __name__ == "__main__":
    unittest.main()
