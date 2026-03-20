#!/bin/bash

SOURCE_DIR="snippets"
TARGET_DIR="output"
PREFIX="${1:-*}"

for script in "$SOURCE_DIR"/$PREFIX*.py; do
    filename=$(basename "$script" .py)
    uv run scripts/trace_comments.py "$script" > "$TARGET_DIR/${filename}.txt" 2>&1
done
