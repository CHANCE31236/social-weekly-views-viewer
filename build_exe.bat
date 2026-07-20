@echo off
cd /d "%~dp0"
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --windowed --name "Social Weekly Views Viewer" social_views_viewer.py
echo.
echo Build finished. Check the dist folder.
pause
