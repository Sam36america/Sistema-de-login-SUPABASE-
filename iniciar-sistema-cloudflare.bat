@echo off
echo ========================================
echo  Iniciando Sistema com Cloudflare Tunnel
echo ========================================
echo.

echo Verificando cloudflared...
if not exist cloudflared.exe (
    echo [ERRO] cloudflared.exe nao encontrado!
    echo.
    echo Execute primeiro: configurar-cloudflare.bat
    echo.
    pause
    exit /b 1
)

echo [1/2] Iniciando API Flask na porta 5000...
cd backend-flask
start "API Flask - Leitor de Faturas" cmd /k "call venv\Scripts\activate && python app.py"
cd ..

echo.
echo [2/2] Aguardando API iniciar...
timeout /t 5 /nobreak > nul

echo.
echo Iniciando Cloudflare Tunnel...
echo.
echo ========================================
echo  IMPORTANTE: Copie a URL abaixo!
echo ========================================
echo.

start "Cloudflare Tunnel" cmd /k "cloudflared.exe tunnel --url http://localhost:5000"

echo.
echo A URL do tunel aparecera na janela "Cloudflare Tunnel"
echo Procure por uma linha tipo:
echo  https://xxxxx.trycloudflare.com
echo.
echo Use essa URL para configurar:
echo  - Frontend (.env.local): NEXT_PUBLIC_API_URL=https://xxxxx.trycloudflare.com
echo  - Vercel (Environment Variables): NEXT_PUBLIC_API_URL=https://xxxxx.trycloudflare.com
echo.
echo ========================================
echo  Sistema iniciado!
echo ========================================
echo.
echo Para parar o sistema:
echo  - Execute: parar-sistema.bat
echo.
pause
