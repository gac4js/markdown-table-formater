#!/usr/bin/env python3
"""Format markdown table column widths."""

import argparse
import re
import sys
import unicodedata

_ESCAPED_PIPE = '\x00'  # placeholder for \| inside cells


def display_width(s: str) -> int:
    """Return the terminal display width of s (wide chars count as 2)."""
    width = 0
    for c in s:
        eaw = unicodedata.east_asian_width(c)
        if eaw in ('W', 'F'):
            width += 2
        elif unicodedata.category(c) in ('Mn', 'Me', 'Cf') or ord(c) == 0xFE0F:
            pass  # zero-width combining / variation selectors
        else:
            width += 1
    return width


def is_table_line(line: str) -> bool:
    return line.strip().startswith('|')


def split_cells(line: str) -> list[str]:
    s = line.strip().replace('\\|', _ESCAPED_PIPE)
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.replace(_ESCAPED_PIPE, '\\|') for c in s.split('|')]


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
        width = display_width(cell)
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


def _raw_split(line: str) -> list[str]:
    """Split on | preserving trailing empty cell (from trailing |), removing only leading empty."""
    s = line.strip().replace('\\|', _ESCAPED_PIPE)
    parts = s.split('|')
    if parts and parts[0] == '':
        parts = parts[1:]
    return [p.replace(_ESCAPED_PIPE, '\\|') for p in parts]


def format_table(lines: list[str]) -> list[str]:
    rows = [_raw_split(line) for line in lines]
    max_cols = max((len(row) for row in rows), default=0)

    # Pad short rows with empty trailing cells (matches column(1) behaviour)
    for row in rows:
        while len(row) < max_cols:
            row.append('')

    # column(1) never pads the last column — compute widths for all but the last
    col_widths = [0] * max(max_cols - 1, 0)
    for row in rows:
        for i, cell in enumerate(row[:-1]):
            col_widths[i] = max(col_widths[i], display_width(cell))

    formatted = []
    for line, row in zip(lines, rows):
        cells = [cell + ' ' * (col_widths[i] - display_width(cell)) for i, cell in enumerate(row[:-1])]
        cells.append(row[-1])  # last cell: no padding, preserves trailing | when empty
        formatted.append('|' + '|'.join(cells))

    for i, orig_line in enumerate(lines):
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
        description='Format markdown table column widths.'
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
