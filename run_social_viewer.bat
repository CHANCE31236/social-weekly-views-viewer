@echo off
cd /d "%~dp0"
python social_views_viewer.py
if errorlevel 1 pause
