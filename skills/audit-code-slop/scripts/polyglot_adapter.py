"""Read-only AST metrics for eleven languages, with explicit pinned conventions."""

import hashlib
import importlib.metadata as metadata
from pathlib import Path

from language_profiles import DECISIONS, EXTENSIONS, FUNCTIONS, RULES, grammar_for
from scb_adapter import AnalysisError


BLOCKS = {"statement_block", "block", "compound_statement", "body_statement", "block_body", "statements", "constructor_body"}
WRAPPERS = BLOCKS | {"else_clause", "else", "then", "control_structure_body", "function_body"}
RETURNS = {"return_statement", "return_expression", "return", "jump_expression", "control_transfer_statement"}
IF_NODES = {"if_statement", "if_expression", "if"}
IDENTIFIERS = {"identifier", "simple_identifier", "variable_name"}
SHORT_CIRCUIT = {"&&", "||", "??", "?:", "and", "or"}
BINARY_NODES = {"binary_expression", "binary", "conjunction_expression", "disjunction_expression", "nil_coalescing_expression", "elvis_expression"}


def load_parsers():
    from tree_sitter_language_pack import get_parser
    names = sorted((set(EXTENSIONS) - {"python"}) | {"tsx"})
    parsers = {name: get_parser(name) for name in names}
    # Hash only supported grammar binaries and their loader, not unrelated bundled languages.
    hashes = {}
    for distribution in ("tree-sitter-language-pack", "tree-sitter-c-sharp"):
        dist = metadata.distribution(distribution)
        for file in sorted(dist.files or ()):
            path = Path(file)
            grammar_binary = path.name.split(".")[0] in names and path.suffix in {".so", ".pyd", ".dll", ".dylib"}
            external_binding = distribution == "tree-sitter-c-sharp" and path.suffix in {".so", ".pyd"}
            if grammar_binary or external_binding or (path.name == "__init__.py" and "bindings" not in path.parts):
                hashes[str(file)] = hashlib.sha256(Path(dist.locate_file(file)).read_bytes()).hexdigest()
    if not hashes:
        raise AnalysisError("Cannot fingerprint bundled grammar binaries")
    return parsers, hashes


def is_comment(node):
    return "comment" in node.type


def walk(node, skip=None):
    stack = [node]
    while stack:
        current = stack.pop()
        if is_comment(current) or (current != node and skip and skip(current)):
            continue
        yield current
        stack.extend(reversed(current.children))


def lines_in(node):
    last = node.end_point.row + (node.end_point.column != 0)
    return range(node.start_point.row + 1, last + 1)


def source_lines(node, skip=None):
    lines = set()
    for child in walk(node, skip):
        if child.child_count == 0 and child.text.strip() and child.type not in {"php_tag", "php_end_tag"}:
            lines.update(lines_in(child))
    return lines


def tokens(node):
    return tuple(n.text for n in walk(node) if n.child_count == 0 and n.text.strip())


def body_of(node, language):
    body = node.child_by_field_name("body")
    if body is None:
        body = next((c for c in node.named_children if c.type in {"function_body", "constructor_body", "statements", "arrow_expression_clause"}), None)
    if node.type in {"property_declaration", "indexer_declaration"}:
        # Automatic properties have no executable body. Accessors are measured separately.
        body = next((c for c in node.named_children if c.type == "arrow_expression_clause"), None)
    if node.type == "computed_property":
        body = next((c for c in node.named_children if c.type == "statements"), None)
    return body


def is_function(node, language):
    if node.type not in FUNCTIONS[language] or body_of(node, language) is None:
        return False
    # A Ruby lambda's block is its body, not a second callable.
    return not (language == "ruby" and node.type in {"block", "do_block"} and node.parent and node.parent.type == "lambda")


def function_name(node, language):
    name = node.child_by_field_name("name")
    if name is None and language == "kotlin":
        name = next((c for c in node.named_children if c.type == "simple_identifier"), None)
    if name is None and language == "cpp" and node.type == "function_definition":
        name = node.child_by_field_name("declarator")
        while name is not None and name.child_by_field_name("declarator") is not None:
            name = name.child_by_field_name("declarator")
    if name is None and node.parent is not None:
        parent = node.parent
        if parent.type in {"variable_declarator", "init_declarator", "let_declaration", "property_declaration", "assignment", "assignment_expression"}:
            name = parent.child_by_field_name("name") or parent.child_by_field_name("pattern") or parent.child_by_field_name("left") or parent.child_by_field_name("declarator")
    base = name.text.decode("utf-8") if name is not None else "<" + node.type + ">"
    ancestors = []
    parent = node.parent
    while parent is not None:
        if parent.type in {"class_declaration", "class_definition", "class_specifier", "struct_item", "impl_item", "trait_item", "object_declaration", "module", "class", "singleton_class"} or is_function(parent, language):
            owner = parent.child_by_field_name("name") or parent.child_by_field_name("type")
            if owner is not None:
                ancestors.append(owner.text.decode("utf-8"))
        parent = parent.parent
    return ".".join([*reversed(ancestors), base])


def complexity(node, language):
    count = 1
    for child in walk(node, lambda n: is_function(n, language)):
        if child.is_named and child.type in DECISIONS[language]:
            # Default/catch-all arms do not add a separate decision.
            first = next((c.text for c in child.children if not is_comment(c)), b"")
            if first not in {b"default", b"else", b"_"}:
                count += 1
        # Operators are AST leaves: strings/comments and type syntax cannot impersonate them.
        if child.child_count == 0 and not child.is_named and child.type in SHORT_CIRCUIT and child.parent.type in BINARY_NODES:
            count += 1
    return count


def statements(node):
    children = [c for c in node.named_children if not is_comment(c)]
    if node.type in WRAPPERS and len(children) == 1 and children[0].type in WRAPPERS:
        return statements(children[0])
    return children if node.type in WRAPPERS else [node]


def branches(node, language):
    left = node.child_by_field_name("consequence") or node.child_by_field_name("body")
    right = node.child_by_field_name("alternative")
    if language == "swift":
        children = [c for c in node.named_children if c.type == "statements"]
        if len(children) == 2:
            left, right = children
    return left, right


def returned_boolean(node):
    body = statements(node)
    if len(body) != 1:
        return None
    statement = body[0]
    if statement.type == "expression_statement" and len(statement.named_children) == 1:
        statement = statement.named_children[0]
    if statement.type not in RETURNS:
        return None
    value = [t for t in tokens(statement) if t not in {b";", b"(", b")"}]
    return value[1] if len(value) == 2 and value[0] == b"return" and value[1] in {b"true", b"false"} else None


def assignment_sides(node):
    left = node.child_by_field_name("left") or node.child_by_field_name("target")
    right = node.child_by_field_name("right") or node.child_by_field_name("value") or node.child_by_field_name("result")
    if left is None and right is None and len(node.named_children) == 2:
        left, right = node.named_children
    def unwrap(value):
        while value is not None and value.type in {"expression_list", "directly_assignable_expression"} and len(value.named_children) == 1:
            value = value.named_children[0]
        return value
    return unwrap(left), unwrap(right)


def rule_findings(nodes, language):
    findings = []
    for node in nodes:
        rule = None
        if node.type in IF_NODES:
            left, right = branches(node, language)
            if left is not None and right is not None:
                a, b = returned_boolean(left), returned_boolean(right)
                if a is not None and b is not None and a != b:
                    rule = "redundant-boolean-branch"
                elif statements(left) and statements(right):
                    a = tuple(t for s in statements(left) for t in tokens(s))
                    b = tuple(t for s in statements(right) for t in tokens(s))
                    if a and a == b:
                        rule = "identical-branch-bodies"
        elif node.type in {"assignment", "assignment_expression", "assignment_statement"}:
            left, right = assignment_sides(node)
            if left is not None and right is not None and left.type in IDENTIFIERS and right.type in IDENTIFIERS and left.text == right.text:
                operators = [c.text for c in node.children if not c.is_named]
                if b"=" in operators:
                    rule = "self-assignment"
        if rule:
            findings.append({"rule": rule, "message": RULES[rule], "start": node.start_point.row + 1, "end": max(lines_in(node))})
    return sorted(findings, key=lambda f: (f["start"], f["end"], f["rule"]))


def clone_candidates(nodes):
    """Bottom-up structural hashes avoid materializing every subtree's source."""
    hashes, sizes, candidates = {}, {}, []
    for node in reversed(nodes):
        children = [c for c in node.children if not is_comment(c)]
        kind = node.type
        identifier = "identifier" in kind or kind in {"name", "variable_name"}
        # Normalize literal leaves only, retaining executable interpolation structure.
        literal = not children and ("string" in kind or "literal" in kind or kind in {"integer", "float", "number", "true", "false", "boolean"})
        payload = b"ID" if identifier else b"LITERAL" if literal else node.text if not children else b"".join(hashes[c.id] for c in children)
        hashes[node.id] = hashlib.sha256(kind.encode() + b"\0" + payload).digest()
        sizes[node.id] = sum(sizes[c.id] for c in children) if children else 1
        if kind in BLOCKS and len(statements(node)) >= 2 and sizes[node.id] >= 20 and len(source_lines(node)) >= 3:
            candidates.append((node, hashes[node.id].hex()))
    return candidates


def analyze_group(root, paths, language, parsers):
    rows, clones = [], {}
    for relative in paths:
        raw = (root/relative).read_bytes()
        try:
            source = raw.decode("utf-8-sig").encode("utf-8")
        except UnicodeError as exc:
            raise AnalysisError(f"{relative}: non-Python sources must use UTF-8") from exc
        tree = parsers[grammar_for(relative, language)].parse(source)
        if tree.root_node.has_error:
            errors = [n for n in walk(tree.root_node) if n.is_error or n.is_missing]
            line = errors[0].start_point.row + 1 if errors else 1
            raise AnalysisError(f"Cannot parse {relative}:{line} as {language}; no score produced")
        nodes = list(walk(tree.root_node))
        sloc = source_lines(tree.root_node)
        functions = []
        for node in nodes:
            if is_function(node, language):
                owned = source_lines(node, lambda n: is_function(n, language))
                functions.append({"name": function_name(node, language), "start": node.start_point.row + 1,
                                  "end": max(lines_in(node)), "cc": complexity(node, language), "sloc": len(owned)})
        rules = rule_findings(nodes, language)
        row = {"path": relative, "language": language, "sha256": hashlib.sha256(raw).hexdigest(),
               "sloc_lines": sorted(sloc), "ast_lines": sorted(sloc & {line for f in rules for line in range(f["start"], f["end"] + 1)}),
               "clone_lines": [], "functions": functions, "rules": rules, "clones": []}
        rows.append(row)
        for node, group in clone_candidates(nodes):
            clones.setdefault(group, []).append((row, node.start_point.row + 1, max(lines_in(node))))
    for group, members in sorted(clones.items()):
        # Wrapper nodes can span exactly the same body; keep each physical occurrence once.
        unique = {(r["path"], start, end): (r, start, end) for r, start, end in members}
        members = [unique[key] for key in sorted(unique)]
        if len(members) < 2:
            continue
        for row, start, end in members:
            row["clone_lines"].extend(range(start, end + 1))
            row["clones"].append({"group": group, "start": start, "end": end,
                                  "peers": [{"path": other["path"], "start": begin} for other, begin, finish in members if (other["path"], begin, finish) != (row["path"], start, end)]})
    for row in rows:
        row["clone_lines"] = sorted(set(row["clone_lines"]) & set(row["sloc_lines"]))
        row["clones"].sort(key=lambda c: (c["start"], c["end"], c["group"]))
    return rows
