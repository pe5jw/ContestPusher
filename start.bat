@echo off
:: ContestPusher — Windows starter
setlocal EnableDelayedExpansion

cd /d "%~dp0"

set PORT=8090
if defined CONTESTPUSHER_PORT set PORT=%CONTESTPUSHER_PORT%

:: ── Python check ──
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FOUT] Python niet gevonden.
    echo Installeer via: https://www.python.org/downloads/
    echo Zorg dat je "Add Python to PATH" aanvinkt tijdens installatie.
    pause
    exit /b 1
)

:: ── Virtualenv aanmaken als die er niet is ──
if not exist ".venv\" (
    echo Virtuele omgeving aanmaken...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [FOUT] Kon geen virtuele omgeving aanmaken.
        pause
        exit /b 1
    )
)

:: ── Activeren ──
call .venv\Scripts\activate.bat

:: ── Dependencies installeren ──
python -m pip install --quiet --upgrade pip
python -m pip install --quiet -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo [FOUT] Dependencies installeren mislukt.
    pause
    exit /b 1
)

:: ── Starten via GUI launcher (geen zwart venster) ──
set CONTESTPUSHER_PORT=%PORT%
start "" pythonw tray.py
