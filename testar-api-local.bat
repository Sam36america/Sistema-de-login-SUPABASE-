@echo off
echo ========================================
echo  Testando API Flask Local
echo ========================================
echo.

echo Abrindo navegador em http://localhost:5000
echo.
start http://localhost:5000
start http://localhost:5000/api/health

echo.
echo Se a API estiver rodando, voce vera:
echo  - Pagina de status da API
echo  - Health check
echo.
echo ========================================
pause
