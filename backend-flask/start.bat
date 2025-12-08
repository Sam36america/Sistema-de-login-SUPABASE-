@echo off
echo ========================================
echo   API Flask - Vora Energia
echo   Leitor de Faturas de Gas
echo ========================================
echo.

REM Ativar ambiente virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [OK] Ambiente virtual ativado
) else (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute: python -m venv venv
    pause
    exit
)

echo.
echo Iniciando servidor Flask na porta 5000...
echo.
echo Endpoints disponiveis:
echo   http://localhost:5000/
echo   http://localhost:5000/api/health
echo   http://localhost:5000/api/upload
echo.
echo Pressione CTRL+C para parar o servidor
echo ========================================
echo.

python app.py

pause
