@echo off
cd /d "%~dp0"

set "PYTHON_EXE="

if exist ".venv-1\Scripts\python.exe" (
  set "PYTHON_EXE=.venv-1\Scripts\python.exe"
) else if exist ".venv\Scripts\python.exe" (
  set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
  echo Creating virtual environment...
  py -3 -m venv .venv 2>nul || python -m venv .venv
  set "PYTHON_EXE=.venv\Scripts\python.exe"
)

if not exist "%PYTHON_EXE%" (
  echo Could not find Python virtual environment.
  exit /b 1
)

echo Installing/updating required packages for desktop app...
call "%PYTHON_EXE%" -m pip install kivy requests

echo Starting Kivy desktop app...
call "%PYTHON_EXE%" frontend\index.py
