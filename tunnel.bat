@echo off
title RUSTOM-II UAV Simulator - Public Cloudflare Tunnel
cd /d "%~dp0"

echo ======================================================================
echo       RUSTOM-II MALE UAV SIMULATOR - PUBLIC INTERNET TUNNEL
echo ======================================================================
echo.
echo Starting secure public Cloudflare tunnel to http://localhost:3000 ...
echo Share the generated https://*.trycloudflare.com link with anyone!
echo.
echo Press Ctrl+C anytime to stop public sharing.
echo ======================================================================
echo.
node tunnel.mjs
pause
