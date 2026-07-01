# Claude Code Hook — Automatic Markdown Table Formatting

After each `.md` file modification made by Claude, the Markdown table formatter runs automatically.

## Prerequisites

- `python3` available in PATH
- `markdown-table-formater.py` script installed (simple copy) in `/usr/local/bin/`
- `jq` available in PATH

## Configuration

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "f=$(jq -r '.tool_input.file_path // empty'); case \"$f\" in *.md) python3 /usr/local/bin/markdown-table-formater.py -i \"$f\" 2>/dev/null;; esac || true",
            "statusMessage": "Formatting markdown tables..."
          }
        ]
      }
    ]
  }
}
```

## Notes

- The hook uses POSIX `case` syntax compatible with `/bin/sh` — bash `[[ ]]` is not available in Claude hooks.
- The hook only fires on modifications made by Claude, not on manual edits in the IDE.
- The scope is global (all projects) since the file is `~/.claude/settings.json`.
