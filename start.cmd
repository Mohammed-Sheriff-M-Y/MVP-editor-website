@echo off
setlocal
cd /d "%~dp0"

if /i "%~1"=="web" goto :web
if /i "%~1"=="kivy" goto :desktop
if /i "%~1"=="desktop" goto :desktop

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
  pause
  exit /b 1
)

echo.
echo ========================================
echo          MVP EDITOR - QUICK START
echo ========================================
echo 1^) Start Web App
echo 2^) Start Desktop App ^(Kivy^)
echo 3^) Exit
echo.

set /p CHOICE=Select an option [1-3]: 

if "%CHOICE%"=="1" goto :web
if "%CHOICE%"=="2" goto :desktop
if "%CHOICE%"=="3" goto :end

echo Invalid choice. Please run start.cmd again.
pause
exit /b 1

:web
call start-web.cmd
goto :end

:desktop
call start-kivy.cmd
goto :end

:end
endlocal