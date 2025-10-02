@echo off
title Update All Packages

:: =============================================
:: This script updates packages for various
:: package managers on Windows.
:: Run this script as an Administrator for best results.
:: =============================================

echo.
echo ===================================
echo   Updating All System Packages
echo ===================================
echo.

:: 1. Windows Package Manager (winget)
echo [~] Checking for winget updates...
winget upgrade --all --accept-package-agreements --accept-source-agreements --disable-interactivity
echo [+] Winget packages updated.
echo.

:: 2. Chocolatey Package Manager
echo [~] Checking for Chocolatey updates...
choco upgrade all -y
echo [+] Chocolatey packages updated.
echo.

:: 3. Node Package Manager (npm) - Global packages
echo [~] Checking for global npm package updates...
npm update -g
echo [+] Global npm packages updated.
echo.

:: 4. Python Package Installer (pip)
echo [~] Checking for pip package updates...
:: First, upgrade pip itself
python -m pip install --upgrade pip
:: Then, upgrade all outdated packages
for /f "delims== " %%i in ('pip list --outdated --format=freeze') do pip install -U %%i
echo [+] Pip packages updated.
echo.


echo ===================================
echo   All updates are complete!
echo ===================================
echo.

pause
