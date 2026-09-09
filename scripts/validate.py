#!/usr/bin/env python3
"""Compile the pinned parser and validate Zed queries. Requires Git, a C compiler,
Python 3.10+, and requirements-dev.txt. Temporary build files are removed on exit.
"""
import argparse
import ctypes
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
try:
    import tomllib
except ImportError:
    import tomli as tomllib
from tree_sitter import Language, Parser, Query, QueryCursor

ROOT = Path(__file__).resolve().parents[1]


def run(*args):
    return subprocess.check_output(args, text=True).strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--grammar-dir', type=Path, help='Use an existing checkout at the exact pinned revision')
    args = ap.parse_args()
    manifest = tomllib.loads((ROOT / 'extension.toml').read_text())
    config = tomllib.loads((ROOT / 'languages/antlr4/config.toml').read_text())
    require(manifest['schema_version'] == 1, 'Unexpected manifest schema')
    require(manifest['id'] == 'antlr4', 'Unexpected extension ID')
    require(config['name'] == 'ANTLR4' and config['path_suffixes'] == ['g4'], 'Incorrect language association')
    grammar = manifest['grammars'][config['grammar']]
    require(re.fullmatch(r'[a-f0-9]{40}', grammar['rev']), 'Grammar must be pinned to a full commit SHA')
    for path in ['README.md', 'LICENSE', 'languages/antlr4/highlights.scm',
                 'languages/antlr4/indents.scm', 'languages/antlr4/brackets.scm']:
        require((ROOT / path).is_file(), f'Missing {path}')
    with tempfile.TemporaryDirectory(prefix='zed-antlr4-') as temp:
        temp = Path(temp)
        source = args.grammar_dir.resolve() if args.grammar_dir else temp / 'grammar'
        if not args.grammar_dir:
            run('git', 'init', '-q', str(source))
            run('git', '-C', str(source), 'fetch', '-q', '--depth=1', grammar['repository'], grammar['rev'])
            run('git', '-C', str(source), 'checkout', '-q', '--detach', 'FETCH_HEAD')
        require(run('git', '-C', str(source), 'rev-parse', 'HEAD') == grammar['rev'], 'Wrong grammar revision')
        require(not run('git', '-C', str(source), 'status', '--porcelain', '--untracked-files=no'), 'Grammar checkout has modified tracked files')
        libpath = temp / ('antlr4.dylib' if sys.platform == 'darwin' else 'antlr4.so')
        compiler = shlex.split(os.environ.get('CC', 'cc'))
        run(*compiler, '-shared', '-fPIC', '-std=c11', '-I', str(source / 'src'),
            str(source / 'src/parser.c'), '-o', str(libpath))
        library = ctypes.CDLL(str(libpath))
        library.tree_sitter_antlr4.restype = ctypes.c_void_p
        capsule = ctypes.pythonapi.PyCapsule_New
        capsule.restype = ctypes.py_object
        capsule.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
        language = Language(capsule(library.tree_sitter_antlr4(), b'tree_sitter.Language', None))
        parser = Parser(language)
        queries = {p.stem: Query(language, p.read_text())
                   for p in sorted((ROOT / 'languages/antlr4').glob('*.scm'))}
        print(f'Manifest and language TOML valid; parser ABI {language.abi_version}; {len(queries)} queries compile.')
        results = {}
        for fixture in sorted((ROOT / 'examples').glob('*.g4')):
            source_bytes = fixture.read_bytes()
            tree = parser.parse(source_bytes)
            require(not tree.root_node.has_error, f'Parse error in {fixture.name}: {tree.root_node}')
            captures = {name: QueryCursor(query).captures(tree.root_node) for name, query in queries.items()}
            results[fixture.name] = captures
            for _, match in QueryCursor(queries['brackets']).matches(tree.root_node):
                require(len(match['open']) == len(match['close']) == 1, 'Unpaired bracket capture')
                require(match['open'][0].end_byte <= match['close'][0].start_byte, 'Reversed brackets')
            for _, match in QueryCursor(queries['indents']).matches(tree.root_node):
                require(match['start'][0].end_byte <= match['end'][0].start_byte, 'Reversed indent range')
            print(f'{fixture.name}: no parse errors; all queries execute.')
        def expect(file, query, capture, text):
            found = {n.text.decode() for n in results[file][query].get(capture, [])}
            require(text in found, f'{file}: expected {query} @{capture} for {text!r}; got {found}')
        for capture, text in [('keyword', 'grammar'), ('type', 'Example'), ('function', 'expression'),
                              ('constant', 'INT'), ('constant.builtin', 'EOF'), ('label', 'left'),
                              ('label', 'Binary'), ('keyword', 'skip'), ('property', 'language'),
                              ('string', "'+'"), ('string.regex', '[a-zA-Z_]'),
                              ('comment.doc', '/** A small expression grammar. */'),
                              ('embedded', '{ int count = 0; }')]:
            expect('Example.g4', 'highlights', capture, text)
        expect('ModesLexer.g4', 'highlights', 'label', 'TAG')
        expect('ModesLexer.g4', 'highlights', 'keyword', 'pushMode')
        expect('ActionsParser.g4', 'highlights', 'embedded', '[int limit]')
        expect('Example.g4', 'brackets', 'open', '(')
        expect('Example.g4', 'indents', 'start', ':')
        expect('Example.g4', 'indents', 'end', ';')
        expect('Example.g4', 'overrides', 'string', "'+'")
        print('PASS: representative highlight, bracket, indentation, and scope assertions.')


if __name__ == '__main__':
    main()
