@echo off
chcp 65001 >nul
setlocal EnableExtensions

cd /d "%~dp0"

where powershell >nul 2>nul
if errorlevel 1 (
  echo.
  echo ERROR: Windows PowerShell is missing. This launcher needs normal Windows PowerShell.
  echo.
  pause
  exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\portable_start.ps1"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo Launcher failed with code %EXIT_CODE%.
  echo Check the error above, then run START.bat again.
  echo.
  pause
)

exit /b %EXIT_CODE%
