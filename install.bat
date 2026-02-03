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

REM Check if ffmpeg is installed (required for M4A support)
echo.
echo Checking for ffmpeg...
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] ffmpeg not found!
    echo ffmpeg is required for M4A file support.
    echo.
    echo To install ffmpeg:
    echo   1. Download from: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    echo   2. Extract the zip file
    echo   3. Add the "bin" folder to your PATH environment variable
    echo.
    echo Or use a package manager like Chocolatey or Scoop:
    echo   choco install ffmpeg
    echo   scoop install ffmpeg
    echo.
    echo Press any key to continue without ffmpeg (M4A files will not work)...
    pause >nul
) else (
    echo [OK] ffmpeg is already installed
    ffmpeg -version 2^>nul ^| findstr "ffmpeg version"
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
echo      python src\main.py path\to\audio.wav
echo.
echo Supported formats: WAV, MP3, FLAC, OGG, M4A
echo.
pause
