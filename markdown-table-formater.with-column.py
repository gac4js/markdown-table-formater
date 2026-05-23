#!/usr/bin/env python3
"""Format markdown table column widths using column(1)."""

import argparse
import re
import subprocess
import sys


def is_table_line(line: str) -> bool:
    return line.strip().startswith('|')


def split_cells(line: str) -> list[str]:
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return s.split('|')


def is_separator_cells(cells: list[str]) -> bool:
    return bool(cells) and all(
        re.fullmatch(r'\s*:?-+:?\s*', c) for c in cells if c.strip()
    )


def rebuild_separator(formatted_line: str, orig_line: str) -> str:
    """Replace separator cell content with dashes matching column width."""
    orig_cells = split_cells(orig_line)
    fmt_cells = split_cells(formatted_line)

    new_cells = []
    for i, cell in enumerate(fmt_cells):
        width = len(cell)
        orig = orig_cells[i].strip() if i < len(orig_cells) else '-'
        left_colon = orig.startswith(':')
        right_colon = orig.endswith(':')
        inner_width = width - left_colon - right_colon
        dashes = '-' * max(inner_width, 1)
        new_cells.append(
            (':' if left_colon else '') + dashes + (':' if right_colon else '')
        )

    s = formatted_line.strip()
    lead = '|' if s.startswith('|') else ''
    trail = '|' if s.endswith('|') else ''
    return lead + '|'.join(new_cells) + trail


def format_table(lines: list[str]) -> list[str]:
    result = subprocess.run(
        ['column', '-s', '|', '-o', '|', '-t'],
        input='\n'.join(lines) + '\n',
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return lines

    formatted = result.stdout.rstrip('\n').split('\n')

    for i, orig_line in enumerate(lines):
        if i >= len(formatted):
            break
        if is_separator_cells(split_cells(orig_line)):
            formatted[i] = rebuild_separator(formatted[i], orig_line)

    return formatted


def process(text: str) -> str:
    out_lines: list[str] = []
    table_buf: list[str] = []

    def flush() -> None:
        if table_buf:
            out_lines.extend(format_table(table_buf))
            table_buf.clear()

    for line in text.splitlines():
        if is_table_line(line):
            table_buf.append(line)
        else:
            flush()
            out_lines.append(line)
    flush()

    result = '\n'.join(out_lines)
    if text.endswith('\n'):
        result += '\n'
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Format markdown table column widths using column(1).'
    )
    parser.add_argument('files', nargs='+', metavar='FILE')
    parser.add_argument(
        '-i', '--inplace',
        action='store_true',
        help='modify files in place instead of printing to stdout',
    )
    args = parser.parse_args()

    for path in args.files:
        try:
            with open(path) as f:
                original = f.read()
        except OSError as e:
            print(f'error: {e}', file=sys.stderr)
            sys.exit(1)

        formatted = process(original)

        if args.inplace:
            with open(path, 'w') as f:
                f.write(formatted)
        else:
            if len(args.files) > 1:
                sys.stdout.write(f'==> {path} <==\n')
            sys.stdout.write(formatted)


if __name__ == '__main__':
    main()
