@echo off
title RUSTOM-II MALE UAV Simulator - Live Internet Host
cd /d "%~dp0"

echo ======================================================================
echo       RUSTOM-II MALE UAV SIMULATOR - COMPLETE LIVE HOST LAUNCHER
echo ======================================================================
echo.
echo [1/2] Starting local simulation & C2 server on http://localhost:3000 ...
start "RUSTOM-II Server" cmd /k "cd /d ""%~dp0"" && python host.py"

echo [2/2] Launching secure public Cloudflare live tunnel ...
timeout /t 3 /nobreak >nul
start "RUSTOM-II Public Tunnel" cmd /k "cd /d ""%~dp0"" && node tunnel.mjs"

echo.
echo ======================================================================
echo Server and Tunnel launched in separate windows!
echo Keep both windows open to keep your simulation live on the internet.
echo ======================================================================
