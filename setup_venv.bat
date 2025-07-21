@echo off
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
@echo.
echo Virtual environment setup complete. To activate later, run:
echo   venv\Scripts\activate 