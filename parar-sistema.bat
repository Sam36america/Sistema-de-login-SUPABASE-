@echo off
echo ========================================
echo  Parando Sistema de Leitura de Faturas
echo ========================================
echo.

echo [1/4] Parando API Flask...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
    if !errorlevel! equ 0 (
        echo  - API Flask parada (PID: %%a)
    )
)

echo.
echo [2/4] Parando Frontend Next.js...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /F /PID %%a 2>nul
    if !errorlevel! equ 0 (
        echo  - Frontend parado (PID: %%a)
    )
)

echo.
echo [3/4] Parando ngrok...
taskkill /F /IM ngrok.exe 2>nul
if %errorlevel% equ 0 (
    echo  - ngrok parado
) else (
    echo  - ngrok nao estava rodando
)

echo.
echo [4/4] Parando Cloudflare Tunnel...
taskkill /F /IM cloudflared.exe 2>nul
if %errorlevel% equ 0 (
    echo  - Cloudflare Tunnel parado
) else (
    echo  - Cloudflare Tunnel nao estava rodando
)

echo.
echo ========================================
echo  Sistema parado com sucesso!
echo ========================================
echo.
pause
