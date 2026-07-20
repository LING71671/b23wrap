@echo off
cd /d "%~dp0"
echo Starting web2bilibili on http://127.0.0.1:8765/
python app\server.py --host 127.0.0.1 --port 8765
pause
