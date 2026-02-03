@echo off
setlocal enabledelayedexpansion

echo ======================================
echo Spectrogrammer Installation Script
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Downloading and installing Python...
    echo.
    
    REM Download Python installer
    echo Downloading Python 3.12...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python_installer.exe'}"
    
    REM Install Python silently
    echo Installing Python...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    
    REM Clean up installer
    del python_installer.exe
    
    echo Python installation complete.
    echo Please close this window and run install.bat again.
    pause
    exit
) else (
    echo [OK] Python is already installed
    python --version
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ======================================
echo Installation complete!
echo ======================================
echo.
echo To use Spectrogrammer:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate.bat
echo   2. Run the program:
echo      python main.py
echo.
pause
