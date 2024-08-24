@echo off
setlocal

set PYTHON_FILE=main.py
set EXE_NAME=sudoku
set TARGET_DIR=release
set OS_DIR=%TARGET_DIR%\windows

pyinstaller --onefile --name "%EXE_NAME%" "%PYTHON_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo Build successful!

    if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"
    if not exist "%OS_DIR%" mkdir "%OS_DIR%"

    move /Y "dist\%EXE_NAME%.exe" "%OS_DIR%"

    rmdir /S /Q build
    rmdir /S /Q dist
    del /Q "%EXE_NAME%.spec"
) else (
    echo Build failed with error code %ERRORLEVEL%.
)

endlocal
