@echo off
:: ------------------------
:: KUDU Deployment Script
:: ------------------------

:: Prerequisites
:: -------------
:: Verify Python Version
python --version
IF %ERRORLEVEL% NEQ 0 (
  echo Python is not installed or the virtual environment is not activated.
  goto error
)

:: Setup
:: -----
setlocal enabledelayedexpansion
SET ARTIFACTS=%~dp0%..\artifacts

:: The path to the Python interpreter
SET PYTHON_DIR=%ARTIFACTS%\env\Scripts

IF NOT EXIST "%PYTHON_DIR%" (
  echo Creating Python virtual environment.
  python -m venv %ARTIFACTS%\env
)

:: Activate the virtual environment
call %ARTIFACTS%\env\Scripts\activate

:: Install Python packages
echo Pip install requirements.
pip install -r requirements.txt

:: Run database migrations
echo Running manage.py migrate
python manage.py migrate --noinput

:: Collect static files
echo Running manage.py collectstatic
python manage.py collectstatic --noinput

:: Done
echo Deployment successful.
goto end

:error
echo An error occurred during deployment.
goto end

:end
endlocal
