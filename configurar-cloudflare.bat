@echo off
echo ========================================
echo  Configuracao Inicial - Cloudflare Tunnel
echo ========================================
echo.

echo Verificando se cloudflared esta instalado...
if not exist cloudflared.exe (
    echo.
    echo [ERRO] cloudflared.exe nao encontrado!
    echo.
    echo Por favor, baixe o cloudflared:
    echo 1. Acesse: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
    echo 2. Baixe a versao Windows 64-bit
    echo 3. Coloque o arquivo cloudflared.exe nesta pasta:
    echo    %CD%
    echo.
    echo OU execute este comando no PowerShell (como administrador):
    echo Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "%CD%\cloudflared.exe"
    echo.
    pause
    exit /b 1
)

echo Cloudflared encontrado!
echo.
echo ========================================
echo  Etapa 1: Fazer login na Cloudflare
echo ========================================
echo.
echo O navegador vai abrir para voce fazer login.
echo Apos fazer login, volte para esta janela.
echo.
pause

cloudflared.exe tunnel login

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha ao fazer login!
    echo.
    echo Tente novamente ou verifique sua conexao com a internet.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Login realizado com sucesso!
echo ========================================
echo.
echo Agora voce pode usar o script:
echo  - iniciar-sistema-cloudflare.bat
echo.
echo A URL do tunel sera exibida quando voce iniciar o sistema.
echo.
pause
