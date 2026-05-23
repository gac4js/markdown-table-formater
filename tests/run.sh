#!/usr/bin/env bash
cd "$(dirname "$0")/.."
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/ "$@"
