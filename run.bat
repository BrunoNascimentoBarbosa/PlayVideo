@echo off
echo Starting VideoPlay Server...
echo.
echo Access the site at http://127.0.0.1:8000
echo Access admin panel at http://127.0.0.1:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo.

IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) ELSE (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Installing dependencies...
    pip install -r requirements.txt
    
    echo Running initial migrations...
    python manage.py migrate
    
    echo.
    echo Please run this script again to start the server.
    echo.
    pause
    exit
)

python manage.py runserver 