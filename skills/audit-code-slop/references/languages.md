# Language support and detector profiles

## Supported source

The analyzer runs in an isolated Python 3.12 environment. It reads these target languages without requiring their compilers, project dependencies, or runtimes:

| Language and CLI name | Source selection | Executable function coverage |
|---|---|---|
| Python: `python` | `.py`, `.pyw` | Functions, async functions, methods under the preserved upstream profile |
| JavaScript: `javascript` | `.js`, `.jsx`, `.mjs`, `.cjs` | Functions, generators, methods, arrows, callbacks; JSX expressions included |
| TypeScript: `typescript` | `.ts`, `.tsx`, `.mts`, `.cts` | JavaScript forms plus typed signatures; TSX uses its own grammar |
| Go: `go` | `.go` | Functions, methods, function literals |
| Rust: `rust` | `.rs` | Functions, impl methods, closures |
| C#/.NET: `csharp` | `.cs`, `.csx` | Methods, constructors, operators, local functions, lambdas, explicit accessors, expression-bodied properties/methods |
| C++: `cpp` | `.cpp`, `.cc`, `.cxx`, `.c++`, `.h`, `.hpp`, `.hh`, `.hxx` | Function definitions, methods, constructors/destructors, lambdas |
| PHP: `php` | `.php`, `.php7`, `.php8`, `.phtml` | Functions, methods, anonymous functions, arrow functions |
| Ruby: `ruby` | `.rb`, `.rake`, `.gemspec`; `Gemfile`, `Rakefile`, `Guardfile` | Methods, singleton methods, lambdas, callable blocks |
| Kotlin: `kotlin` | `.kt`, `.kts` | Functions, expression bodies, anonymous functions, lambdas, explicit accessors, secondary constructors, initializer bodies |
| Swift: `swift` | `.swift` | Functions, initializers/deinitializers, closures, computed properties and explicit accessors |
| Java: `java` | `.java` | Methods, constructors, compact constructors, lambdas |

Extensions are case-insensitive. `.h` is interpreted as C++; standalone C and Objective-C are outside the supported set. TypeScript declaration-only files are included in source inventory but have no executable function mass, so their erosion is null. Review their contribution to the verbosity denominator. Anonymous and overloaded functions use location-backed occurrence identities; not every inferred function label is a compiler-qualified symbol.

The C# profile covers C# source used by .NET, not all .NET languages or artifacts. F#, VB.NET, Razor/CSHTML, Vue/Svelte single-file components, Ruby ERB, binaries, and other recognized unsupported formats are unscored. Embedded-language extraction is not implemented. PHP mixed markup can contribute source lines, but only PHP grammar functions receive complexity measurements. Unknown file extensions are not automatically classified. Tell the user what was excluded or left unscored.

## Detector breadth

Python retains the `python-scb-0.2.0-two-term/1` detector semantics. The other eleven languages use `tree-sitter-core-rules/1`, implemented against grammars bundled in tree-sitter-language-pack 0.10.0. The package is deliberately pinned to a release that bundles parsers, so analysis performs no on-demand grammar downloads.

Each added language has three AST rules, verified with positive source fixtures in every language:

| Rule | Evidence | Interpretation |
|---|---|---|
| `redundant-boolean-branch` | An if/else whose sole statements explicitly return opposite Boolean literals | A direct Boolean result may express the same intent; preserve coercion and condition side effects |
| `identical-branch-bodies` | Both branch bodies have identical executable tokens, preserving names and literal values | Inspect whether the branch can be removed without losing necessary condition evaluation |
| `self-assignment` | A plain variable is assigned to itself with `=` | Inspect redundancy; member/property assignments and compound assignments are excluded |

These rules run directly on parsed trees. Their flagged-line set fills the same role as ast-grep findings in the verbosity formula. They are a smaller independently authored profile, not translations of all 197 Python rules and not a reproduction of the research detector. Scores reflect their limited coverage. Findings remain review candidates; language semantics can make a seemingly redundant construct intentional.

Structural clone detection supplements the three rules. It hashes block ASTs while normalizing identifiers and literal leaves, retaining operators and executable interpolation structure. Candidates require at least two direct statements, 20 syntax leaves, and three measured source lines. Matching bodies can span different files or functions, but must share the language and production/test group. JavaScript and TypeScript are separate clone domains; JSX belongs to JavaScript and TSX to TypeScript. Clone findings are unions of locations, so nested matches cannot multiply a line's contribution.

## Complexity and source-line conventions

The added languages use a syntax-based CC variant: one plus recognized conditional branches, loops, nondefault case/arm groups, handlers, ternaries, and short-circuit/coalescing operators. These are profile conventions, not compiler control-flow proofs. A switch arm with several labels is counted as one decision where the grammar groups them. Unconditional loops and language-specific constructs may differ from other CC tools. The fixed grammar node sets live in the language profile script and are part of the fingerprinted implementation.

Named and anonymous executable functions have separate records. Unlike the preserved Python profile, nested callables use **exclusive** accounting: their bodies do not inflate their enclosing function's CC or source-line mass. A Ruby lambda's block body is not counted twice. Function declarations without implementations, automatic properties, and interface signatures do not create artificial low-CC function records. Top-level statements contribute verbosity but not function mass.

Source lines are physical line locations covered by noncomment syntax leaves. Blank/comment-only lines are omitted; brace-only lines and lines covered by multiline string tokens count. PHP opening/closing tag tokens are omitted where represented as those grammar tokens. This differs from Python's token-start SLOC convention. Do not treat a code migration between languages as a like-for-like metric improvement.

## Practical limits

- Parsing is syntax-only. It does not resolve types, compile conditional builds, expand C++/Rust macros, inspect reflection, or validate runtime behavior. Opaque macro token bodies are not parsed as executable functions. Run the project's own relevant checks for behavior verification.
- New language syntax is supported only when the pinned grammar recognizes it. Any parser error/missing syntax makes the entire scan unavailable; error recovery cannot silently produce clean scores. Non-Python sources require UTF-8, with an optional BOM.
- Physical line counts and the clone size threshold are formatting-sensitive. Minifying code can change the ratios without improving maintenance. Some valid compact Kotlin forms are rejected by the pinned grammar's automatic-semicolon handling; treat that as unavailable analysis, not invalid application code.
- Test classification is file-based. Common test/spec names and directories are recognized, including TS/JS `.test`/`.spec`, Go `_test.go`, C#/Swift `Tests`, Ruby specs, and Java/Kotlin test trees. Rust tests inside a production `.rs` file remain in that file's group. Use `--test-glob` for project conventions and explain mixed files.
- Language selection, test classification, tool versions, parser binaries, rules, and analyzer code are fingerprinted. The multilingual profile changes the baseline contract: remeasure both snapshots to compare new scans with older Python-only work. Legacy JSON remains readable, and two compatible legacy reports can still be compared.
- No profile has validated universal pass/fail thresholds. Calibrate each language and code role within the project. Mixed totals are descriptive and sensitive to changing language proportions; inspect the per-language breakdown and raw burden before claiming improvement.
