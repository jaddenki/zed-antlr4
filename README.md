# ANTLR4 for Zed

Syntax highlighting, indentation, and bracket matching for ANTLR4 `.g4` files.
Includes comment toggling and automatic bracket closing.

Parser rules, lexer tokens, labels, options, commands, strings, character sets,
and comments use separate highlight captures. Colors depend on your Zed theme.

## Installation

Install from source as a Zed dev extension:

```sh
git clone https://github.com/jaddenki/zed-antlr4.git
```

In Zed, run **zed: install dev extension** from the command palette and select
the cloned folder. Open `examples/Example.g4`; the language indicator should
show **ANTLR4**.

Zed downloads and compiles the grammar on first installation, so Git and network
access are required. See Zed's [development prerequisites](https://zed.dev/docs/extensions/developing-extensions)
for toolchain setup. If installation fails, run **zed: open log**.

After editing the extension, use **Rebuild** in Zed's Extensions page.

## Grammar

Uses [lakitu/tree-sitter-antlr4](https://github.com/lakitu/tree-sitter-antlr4),
pinned in `extension.toml`. Zed builds the upstream parser as WebAssembly.
This extension does not require Rust extension code or a language server.

## Limitations

- Embedded actions and arguments have a single highlight style, without
  target-language syntax highlighting.
- Strings and lexer character sets are single tokens in the upstream grammar.
  Their escapes and internal brackets are not highlighted separately.
- Indentation covers rule bodies and delimited blocks; it does not format files.
- Parser coverage and error recovery depend on the upstream grammar.
- Completion, diagnostics, and ANTLR code generation are not included.

## Development

The language configuration and queries are in `languages/antlr4/`. The
`examples/` folder covers combined grammars, lexer modes, and parser actions.
These are syntax fixtures, not a complete ANTLR application.

To validate on macOS or Linux, install Python 3.10+, Git, and a C compiler:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

The script fetches the pinned grammar, compiles its C parser, checks the TOML
files and all queries, and verifies captures against the examples. To reuse a
clean checkout at the pinned revision, pass `--grammar-dir /path/to/grammar`.

See [VALIDATION.md](VALIDATION.md) for test results.

## License

[MIT](LICENSE). The upstream Tree-sitter grammar declares MIT in its package
metadata and source header; credit belongs to its contributors.
