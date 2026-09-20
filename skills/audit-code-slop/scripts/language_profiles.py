"""Versioned source inventory and grammar conventions; no runtime dependencies."""

from pathlib import Path


EXTENSIONS = {
    "python": (".py", ".pyw"),
    "javascript": (".js", ".jsx", ".mjs", ".cjs"),
    "typescript": (".ts", ".tsx", ".mts", ".cts"),
    "go": (".go",), "rust": (".rs",), "csharp": (".cs", ".csx"),
    "cpp": (".cpp", ".cc", ".cxx", ".c++", ".h", ".hpp", ".hh", ".hxx"),
    "php": (".php", ".php8", ".php7", ".phtml"), "ruby": (".rb", ".rake", ".gemspec"),
    "kotlin": (".kt", ".kts"), "swift": (".swift",), "java": (".java",),
}

FUNCTIONS = {
    "javascript": {"function_declaration", "function_expression", "generator_function", "generator_function_declaration", "arrow_function", "method_definition"},
    "typescript": {"function_declaration", "function_expression", "generator_function", "generator_function_declaration", "arrow_function", "method_definition"},
    "go": {"function_declaration", "method_declaration", "func_literal"},
    "rust": {"function_item", "closure_expression"},
    "csharp": {"method_declaration", "constructor_declaration", "destructor_declaration", "operator_declaration", "conversion_operator_declaration", "local_function_statement", "lambda_expression", "anonymous_method_expression", "accessor_declaration", "property_declaration", "indexer_declaration"},
    "cpp": {"function_definition", "lambda_expression"},
    "php": {"function_definition", "method_declaration", "anonymous_function", "arrow_function"},
    "ruby": {"method", "singleton_method", "lambda", "block", "do_block"},
    "kotlin": {"function_declaration", "secondary_constructor", "anonymous_function", "lambda_literal", "getter", "setter", "anonymous_initializer"},
    "swift": {"function_declaration", "init_declaration", "deinit_declaration", "lambda_literal", "computed_getter", "computed_setter", "computed_modify", "computed_property"},
    "java": {"method_declaration", "constructor_declaration", "compact_constructor_declaration", "lambda_expression"},
}

DECISIONS = {
    "javascript": {"if_statement", "for_statement", "for_in_statement", "while_statement", "do_statement", "switch_case", "catch_clause", "ternary_expression"},
    "typescript": {"if_statement", "for_statement", "for_in_statement", "while_statement", "do_statement", "switch_case", "catch_clause", "ternary_expression"},
    "go": {"if_statement", "for_statement", "expression_case", "type_case", "communication_case"},
    "rust": {"if_expression", "while_expression", "for_expression", "match_arm"},
    "csharp": {"if_statement", "for_statement", "foreach_statement", "while_statement", "do_statement", "catch_clause", "catch_filter_clause", "conditional_expression", "switch_section", "switch_expression_arm", "when_clause"},
    "cpp": {"if_statement", "for_statement", "for_range_loop", "while_statement", "do_statement", "case_statement", "catch_clause", "conditional_expression"},
    "php": {"if_statement", "else_if_clause", "for_statement", "foreach_statement", "while_statement", "do_statement", "case_statement", "catch_clause", "conditional_expression", "match_conditional_expression"},
    "ruby": {"if", "elsif", "unless", "if_modifier", "unless_modifier", "while", "until", "while_modifier", "until_modifier", "for", "when", "in", "if_guard", "unless_guard", "rescue", "rescue_modifier", "conditional"},
    "kotlin": {"if_expression", "for_statement", "while_statement", "do_while_statement", "when_entry", "catch_block"},
    "swift": {"if_statement", "guard_statement", "for_statement", "while_statement", "repeat_while_statement", "switch_entry", "catch_block", "ternary_expression"},
    "java": {"if_statement", "for_statement", "enhanced_for_statement", "while_statement", "do_statement", "switch_label", "catch_clause", "ternary_expression", "guard"},
}

RULES = {
    "redundant-boolean-branch": "Opposite literal Boolean returns in a two-way branch; consider a direct Boolean result.",
    "identical-branch-bodies": "Both sides have the same executable tokens; inspect whether the branch is necessary.",
    "self-assignment": "A simple variable is assigned to itself; inspect whether this is redundant.",
}
POLYGLOT_PROFILE = "tree-sitter-core-rules/1"


def language_for(path):
    path = Path(path)
    if path.name in {"Gemfile", "Rakefile", "Guardfile"}:
        return "ruby"
    return next((name for name, suffixes in EXTENSIONS.items() if path.suffix.lower() in suffixes), None)


def grammar_for(path, language):
    return "tsx" if language == "typescript" and Path(path).suffix.lower() == ".tsx" else language
