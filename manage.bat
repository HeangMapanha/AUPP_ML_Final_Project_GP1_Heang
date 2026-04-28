@echo off
set ROOT=%~dp0
set NGROK_URL=Not started yet
set STATUS=OFFLINE
:: Show menu if no argument given
if "%1"=="" goto MENU

:: Handle commands
if "%1"=="start"   goto START
if "%1"=="stop"    goto STOP
if "%1"=="install" goto INSTALL
echo Unknown command: %1


:MENU
cls
echo ================================
echo   App Manager ^|^| Server: %STATUS%
echo ================================
echo   Ngrok Public Link: 
echo  %NGROK_URL%
echo ================================
echo  install  - Install all packages
echo  start    - Start all apps
echo  stop     - Stop all apps
echo ================================
set /p choice="Enter command: "
if "%choice%"=="install" goto INSTALL
if "%choice%"=="start"   goto START
if "%choice%"=="stop"    goto STOP
goto MENU


:INSTALL
echo Installing FastAPI packages...
cd /d "%ROOT%model"
pip install fastapi uvicorn joblib opencv-python

echo Installing Node.js packages...
cd /d "%ROOT%server"
npm install express axios
npm install -g ngrok

echo ✅ All packages installed!
goto MENU

:START
echo Starting all apps...
start /min "FastAPI" cmd /k "cd /d %ROOT%model && uvicorn API:app --host 0.0.0.0 --port 8000"
start /min "NodeJS"  cmd /k "cd /d %ROOT%server && node server.js"
start /min "Ngrok"   cmd /k "ngrok http 4000"
echo ✅ All apps started!
goto NGROK_LINK

:NGROK_LINK
echo Fetching Ngrok link...
timeout /t 3 >nul

for /f "usebackq delims=" %%a in (`curl -s http://localhost:4040/api/tunnels ^| python -c "import sys,json; print(json.load(sys.stdin)['tunnels'][0]['public_url'])"`) do set NGROK_URL=%%a
timeout /t 2 >nul
set STATUS=ONLINE
goto MENU


:STOP
echo Stopping all apps...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im node.exe   >nul 2>&1
taskkill /f /im ngrok.exe  >nul 2>&1
echo ✅ All apps stopped!

taskkill /f /fi "WINDOWTITLE eq FastAPI" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq NodeJS"  >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Ngrok"   >nul 2>&1

set STATUS=OFFLINE
set NGROK_URL=Not Yet started
goto MENU

:END
pause
