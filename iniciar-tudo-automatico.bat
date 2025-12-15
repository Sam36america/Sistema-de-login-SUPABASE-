@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Sistema de Leitura de Faturas
echo  Inicializacao COMPLETA e AUTOMATICA
echo ========================================
echo.

REM Verificar cloudflared
if not exist cloudflared.exe (
    echo [ERRO] cloudflared.exe nao encontrado!
    echo.
    echo Baixando cloudflared automaticamente...
    echo.

    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe' -OutFile 'cloudflared.exe'"

    if !errorlevel! neq 0 (
        echo.
        echo [ERRO] Falha ao baixar cloudflared!
        echo Por favor, baixe manualmente de:
        echo https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
        echo.
        pause
        exit /b 1
    )

    echo cloudflared baixado com sucesso!
    echo.
)

echo [1/4] Iniciando API Flask...
cd backend-flask
start "API Flask - Leitor de Faturas" cmd /k "call venv\Scripts\activate && python app.py"
cd ..

echo.
echo [2/4] Aguardando API iniciar...
timeout /t 5 /nobreak > nul

echo.
echo [3/4] Iniciando Cloudflare Tunnel...

REM Criar arquivo temporário para o log
set LOGFILE=%TEMP%\cloudflared_output.txt
if exist %LOGFILE% del %LOGFILE%

REM Iniciar cloudflared
start "Cloudflare Tunnel" cmd /c "cloudflared.exe tunnel --url http://localhost:5000 > %LOGFILE% 2>&1"

echo Aguardando URL do Cloudflare...
timeout /t 10 /nobreak > nul

REM Extrair URL
set TUNNEL_URL=
for /L %%i in (1,1,5) do (
    if "!TUNNEL_URL!"=="" (
        for /f "tokens=*" %%a in ('findstr /r "https://.*\.trycloudflare\.com" %LOGFILE% 2^>nul') do (
            set LINE=%%a
            for /f "tokens=*" %%b in ('echo !LINE!') do (
                set TUNNEL_URL=%%b
                goto :url_found
            )
        )
        timeout /t 2 /nobreak > nul
    )
)

:url_found

if "!TUNNEL_URL!"=="" (
    echo.
    echo [AVISO] Nao foi possivel capturar a URL automaticamente.
    echo Verifique a janela "Cloudflare Tunnel" para obter a URL.
    echo.
) else (
    REM Limpar URL (pegar apenas a URL)
    for /f "tokens=*" %%a in ('echo !TUNNEL_URL! ^| findstr /r "https://[a-zA-Z0-9-]*\.trycloudflare\.com"') do (
        set CLEAN_URL=%%a
    )

    if not "!CLEAN_URL!"=="" (
        echo.
        echo ========================================
        echo  URL Capturada: !CLEAN_URL!
        echo ========================================
        echo.

        REM Atualizar .env.local
        echo Atualizando .env.local...

        REM Ler valores do Supabase
        for /f "tokens=1,* delims==" %%a in ('findstr "NEXT_PUBLIC_SUPABASE_URL" .env.local 2^>nul') do set SUPABASE_URL=%%b
        for /f "tokens=1,* delims==" %%a in ('findstr "NEXT_PUBLIC_SUPABASE_ANON_KEY" .env.local 2^>nul') do set SUPABASE_KEY=%%b

        REM Criar novo .env.local
        (
            echo # Supabase Configuration
            echo # Pegar essas informacoes em: https://app.supabase.com/project/SEU_PROJETO/settings/api
            echo.
            echo NEXT_PUBLIC_SUPABASE_URL=!SUPABASE_URL!
            echo NEXT_PUBLIC_SUPABASE_ANON_KEY=!SUPABASE_KEY!
            echo.
            echo # Desabilitar Turbopack ^(tem bug na versao 16.0.7^)
            echo TURBOPACK=0
            echo.
            echo # API Backend ^(Cloudflare Tunnel^)
            echo # Atualizado automaticamente em: %date% %time%
            echo NEXT_PUBLIC_API_URL=!CLEAN_URL!
        ) > .env.local

        echo .env.local atualizado!
    )
)

echo.
echo [4/4] Iniciando Frontend Next.js...
timeout /t 2 /nobreak > nul
start "Frontend Next.js" cmd /k "npm run dev"

echo.
echo ========================================
echo  SISTEMA INICIADO COMPLETAMENTE!
echo ========================================
echo.
echo  3 janelas abertas:
echo  1. API Flask (porta 5000)
echo  2. Cloudflare Tunnel (URL publica)
echo  3. Frontend Next.js (porta 3000)
echo.
if not "!CLEAN_URL!"=="" (
    echo  URL Publica da API: !CLEAN_URL!
)
echo  Frontend Local: http://localhost:3000
echo.
echo Aguarde ~30 segundos para o frontend iniciar...
echo Depois acesse: http://localhost:3000
echo.
echo Para parar tudo: Execute parar-sistema.bat
echo.
pause
