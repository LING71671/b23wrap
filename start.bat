@echo off
cd /d "%~dp0"
echo.
echo  ========================================
echo   b23wrap  -  本机签发服务
echo  ========================================
echo.
echo  请用浏览器打开下面地址（不要用 GitHub Pages 签发）：
echo.
echo      http://127.0.0.1:8765/
echo.
echo  GitHub Pages 是纯静态页，浏览器读不到 B 站签发接口的 JSON
echo  （没有 CORS 头），所以 Pages 上只能出长链。
echo  本机 server.py 会代为请求 B 站，才能签发 b23。
echo.
echo  详见 DISCLAIMER.md · 非 B 站官方产品
echo  ========================================
echo.
start "" "http://127.0.0.1:8765/"
python app\server.py --host 127.0.0.1 --port 8765
if errorlevel 1 (
  echo.
  echo  [错误] 启动失败。请确认已安装 Python 3.10+ 并在 PATH 中。
  pause
)
