@echo off
echo Installing required packages...
python -m pip install -r requirements.txt

echo.
echo Starting QR Code Generator server...
echo Open your browser and go to: http://localhost:5000
echo.
python app.py

pause
