# markdown-table-formater.py

Formats markdown tables by aligning columns, with no external dependencies.

## Usage

```bash
# preview on stdout
python3 markdown-table-formater.py file.md

# in-place modification
python3 markdown-table-formater.py -i file.md

# multiple files
python3 markdown-table-formater.py -i *.md
```

## How it works

The script reads the file line by line, accumulates table blocks (lines starting with `|`), then formats them:

1. Compute the maximum display width of each column (display width, not character count)
2. Pad each cell to that width
3. Regenerate separator lines (`|---|---|`) with full-width dashes, preserving alignment markers (`:---`, `:---:`, `---:`)

The trailing `|` on each line is preserved or omitted based on the original.

## Handled cases

- **Wide characters** (emoji `✅`, `❌`, CJK…): counted as 2 display columns
- **Escaped pipe** (`\|`): treated as a literal character, not a column separator
- **Table without trailing `|`**: the last column is not padded (same behaviour as `column(1)`)
- **Mixed table**: lines without trailing `|` in a table that has them — padded and aligned with the others

## Tests

```bash
tests/run.sh          # runs pytest
tests/run.sh -v       # verbose mode
```

Sample files are in `sample/` (pairs `*.input.md` / `*.expected.md`).
