@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Create a local environment and install dependencies first. See README.md.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" social_views_viewer.py
if errorlevel 1 pause
