@echo off
echo Starting LifeStream Desktop App...
pip install -r requirements.txt >nul 2>&1
python desktop_launcher.py
pause
