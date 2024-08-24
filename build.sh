#!/bin/bash

PYTHON_FILE="main.py"
EXE_NAME="sudoku"
TARGET_DIR="release"
OS_DIR="release/linux"

pyinstaller --onefile --name "$EXE_NAME" "$PYTHON_FILE"

if [ $? -eq 0 ]; then
    echo "Build successful!"
    mkdir -p "$TARGET_DIR"
    mkdir -p "$OS_DIR"
    mv dist/"$EXE_NAME" "$OS_DIR/"
    rm -r build
    rm -r dist
    rm sudoku.spec
fi
