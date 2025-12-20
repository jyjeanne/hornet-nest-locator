#!/bin/bash
# Launch Hornet Nest Locator GUI

cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$PATH"
uv run python gui.py
