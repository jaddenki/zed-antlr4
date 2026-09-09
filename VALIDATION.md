# Validation

Validated on 2026-09-09 on macOS with Python 3.12.14, tree-sitter 0.25.2,
and the system C compiler.

- Parsed `extension.toml` and `config.toml` as TOML and checked language/grammar
  linkage, `.g4` association, required files, and the full grammar commit pin.
- Compiled the pinned upstream `src/parser.c` into a native shared library.
  The resulting parser reports Tree-sitter ABI 14.
- Compiled all four `.scm` files using that parser: highlights, indents,
  brackets, and overrides.
- Parsed all three example grammars without ERROR or missing nodes and executed
  all four queries on each tree.
- Asserted representative captures for keywords, grammar names, parser rules,
  lexer tokens, EOF, labels, options, lexer commands, strings, character sets,
  documentation comments, actions, and arguments.
- Checked bracket capture pairing/order and indentation start/end ordering.
- Ran the validator both against an existing pinned checkout and through its
  default fresh-download path; both passed.
- Cross-checked declarative extension discovery, optional top-level repository
  metadata, and block-comment configuration against Zed's current source.

Result:

```text
Manifest and language TOML valid; parser ABI 14; 4 queries compile.
ActionsParser.g4: no parse errors; all queries execute.
Example.g4: no parse errors; all queries execute.
ModesLexer.g4: no parse errors; all queries execute.
PASS: representative highlight, bracket, indentation, and scope assertions.
```

## Manual testing

The maintainer reported successfully installing this version as a Zed dev
extension and confirmed that highlighting worked. No parser, language
configuration, or query changes were made after that test.

The automated checks above run the native parser, not Zed's UI. They do not
verify every interactive indentation or bracket-closing behavior.
