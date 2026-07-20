@echo off
cd /d "%~dp0"
echo.
echo  b23wrap toolbox  -  http://127.0.0.1:8765/
echo  Read DISCLAIMER.md before use. Not affiliated with Bilibili.
echo.
python app\server.py --host 127.0.0.1 --port 8765
pause
