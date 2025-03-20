@echo off
title HellLogger Launcher

echo Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements! Check your Python setup or requirements.txt.
    pause
    exit /b %ERRORLEVEL%
)

pause
