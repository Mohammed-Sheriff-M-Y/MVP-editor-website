@echo off
setlocal
cd /d "%~dp0"

set "PYTHON_EXE="

if exist ".venv-1\Scripts\python.exe" (
	set "PYTHON_EXE=.venv-1\Scripts\python.exe"
) else if exist ".venv\Scripts\python.exe" (
	set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
	echo Creating virtual environment...
	py -3 -m venv .venv 2>nul || python -m venv .venv
	if exist ".venv\Scripts\python.exe" (
		set "PYTHON_EXE=.venv\Scripts\python.exe"
	)
)

if not exist "%PYTHON_EXE%" (
	echo Could not find Python virtual environment.
	echo Please install Python 3.10+ and run this again.
	exit /b 1
)

echo Installing/updating requirements...
call "%PYTHON_EXE%" -m pip install -r requirements.txt
if errorlevel 1 (
	echo Failed to install requirements.
	exit /b 1
)

echo Starting web app at http://127.0.0.1:5000 ...
call "%PYTHON_EXE%" backend\server.py

endlocal
