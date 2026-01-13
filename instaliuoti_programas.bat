@echo off
echo Instaliuojamos reikiamos programos...
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
echo.
echo Instaliavimas baigtas!
pause
