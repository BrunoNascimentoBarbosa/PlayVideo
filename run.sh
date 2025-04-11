#!/bin/bash

echo "Starting VideoPlay Server..."
echo
echo "Access the site at http://127.0.0.1:8000"
echo "Access admin panel at http://127.0.0.1:8000/admin"
echo
echo "Press Ctrl+C to stop the server"
echo

if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
    
    echo "Running initial migrations..."
    python manage.py migrate
    
    echo
    echo "Please run this script again to start the server."
    echo
    exit 1
fi

python manage.py runserver 