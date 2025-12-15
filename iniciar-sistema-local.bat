@echo off
echo ========================================
echo  Iniciando Sistema LOCALMENTE
echo  (Sem ngrok - Apenas para testes local)
echo ========================================
echo.

echo [1/2] Iniciando API Flask na porta 5000...
cd backend-flask
start "API Flask - Leitor de Faturas" cmd /k "call venv\Scripts\activate && python app.py"

echo.
echo [2/2] Aguardando API iniciar...
timeout /t 5 /nobreak > nul

echo.
echo [3/3] Iniciando Frontend Next.js...
cd ..
start "Frontend Next.js" cmd /k "npm run dev"

echo.
echo ========================================
echo  Sistema LOCAL iniciado com sucesso!
echo ========================================
echo.
echo  Aguarde uns segundos e acesse:
echo  - Frontend: http://localhost:3000
echo  - API Backend: http://localhost:5000
echo.
echo  IMPORTANTE: Funciona apenas neste computador!
echo  Para acessar de outros PCs, use o ngrok.
echo.
pause
