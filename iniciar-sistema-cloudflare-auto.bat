@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Iniciando Sistema com Cloudflare Tunnel
echo  (Modo Automatico)
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

echo [1/3] Iniciando API Flask na porta 5000...
cd backend-flask
start "API Flask - Leitor de Faturas" cmd /k "call venv\Scripts\activate && python app.py"
cd ..

echo.
echo [2/3] Aguardando API iniciar...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Iniciando Cloudflare Tunnel e capturando URL...
echo.

REM Criar arquivo temporário para o log do cloudflared
set LOGFILE=%TEMP%\cloudflared_output.txt

REM Iniciar cloudflared em background e redirecionar saída
start "Cloudflare Tunnel" cmd /c "cloudflared.exe tunnel --url http://localhost:5000 > %LOGFILE% 2>&1"

echo Aguardando URL do Cloudflare Tunnel...
timeout /t 10 /nobreak > nul

REM Tentar extrair a URL do log
set TUNNEL_URL=
for /f "tokens=*" %%i in ('findstr /r "https://.*\.trycloudflare\.com" %LOGFILE%') do (
    set LINE=%%i
    for /f "tokens=*" %%j in ('echo !LINE! ^| findstr /r "https://[^ ]*\.trycloudflare\.com"') do (
        set TUNNEL_URL=%%j
    )
)

if "!TUNNEL_URL!"=="" (
    echo.
    echo [AVISO] Nao foi possivel capturar a URL automaticamente.
    echo.
    echo Por favor, copie manualmente da janela "Cloudflare Tunnel"
    echo e edite o arquivo .env.local
    echo.
    pause
    exit /b 0
)

REM Limpar a URL (remover espaços e caracteres extras)
set TUNNEL_URL=!TUNNEL_URL: =!

echo.
echo ========================================
echo  URL Capturada: !TUNNEL_URL!
echo ========================================
echo.

REM Atualizar .env.local
echo Atualizando .env.local...

REM Criar novo arquivo .env.local
(
    echo # Supabase Configuration
    echo # Pegar essas informacoes em: https://app.supabase.com/project/SEU_PROJETO/settings/api
    echo.
    for /f "tokens=1,* delims==" %%a in ('findstr "NEXT_PUBLIC_SUPABASE" .env.local') do (
        echo %%a=%%b
    )
    echo.
    echo # Desabilitar Turbopack ^(tem bug na versao 16.0.7^)
    echo TURBOPACK=0
    echo.
    echo # API Backend ^(Cloudflare Tunnel^)
    echo # URL atualizada automaticamente em: %date% %time%
    echo NEXT_PUBLIC_API_URL=!TUNNEL_URL!
) > .env.local.tmp

move /y .env.local.tmp .env.local > nul

echo.
echo ========================================
echo  Sistema iniciado com sucesso!
echo ========================================
echo.
echo  - API Flask: http://localhost:5000
echo  - Cloudflare Tunnel: !TUNNEL_URL!
echo  - .env.local atualizado automaticamente
echo.
echo Para usar o sistema:
echo  1. Execute: npm run dev
echo  2. Acesse: http://localhost:3000
echo.
echo Para parar o sistema:
echo  - Execute: parar-sistema.bat
echo.
pause
