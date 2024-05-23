@echo off

:: Check for Python 3
where /R C:\ python.exe > nul
if %ERRORLEVEL% NEQ 0 (
    echo "Python 3 could not be found. Please install Python 3 and try again."
    exit /B
)

:: Create a virtual environment
python -m venv venv

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Run the application
python main.py
