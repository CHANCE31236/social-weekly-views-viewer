@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv
    if errorlevel 1 goto :failed
)
".venv\Scripts\python.exe" -m pip install -r requirements-dev.txt
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 goto :failed
".venv\Scripts\python.exe" -m PyInstaller --onefile --windowed --name "Social Weekly Views Viewer" social_views_viewer.py
if errorlevel 1 goto :failed
echo.
echo Build finished. Check the dist folder.
pause
exit /b 0

:failed
echo Build failed. Review the error above.
pause
exit /b 1
