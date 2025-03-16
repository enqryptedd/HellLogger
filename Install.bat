@echo off
title HellLogger Launcher

echo Installing requirements...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install requirements! Check your Python setup or requirements.txt.
    pause
    exit /b %ERRORLEVEL%
)

echo Launching HellLogger...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo HellLogger crashed! Check the script or your setup.
    pause
    exit /b %ERRORLEVEL%
)

pause