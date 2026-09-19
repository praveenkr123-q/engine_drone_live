@echo off
title RUSTOM-II MALE UAV Simulator
cd /d "%~dp0"

echo ======================================================================
echo           RUSTOM-II MALE UAV SIMULATOR - LAUNCHER
echo ======================================================================
echo.

where python >nul 2>nul
if %errorlevel% equ 0 (
    python host.py
    goto end
)

where npm >nul 2>nul
if %errorlevel% equ 0 (
    echo Launching with Vite Preview...
    npm run preview
    goto end
)

echo [ERROR] Neither Python nor Node.js was found in PATH.
pause

:end
