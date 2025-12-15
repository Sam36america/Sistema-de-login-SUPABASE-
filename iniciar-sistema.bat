@echo off
echo ========================================
echo  Iniciando Sistema de Leitura de Faturas
echo ========================================
echo.

echo [1/3] Ativando ambiente virtual Python...
cd backend-flask
call venv\Scripts\activate

echo.
echo [2/3] Iniciando API Flask na porta 5000...
start "API Flask - Leitor de Faturas" cmd /k "python app.py"

echo.
echo [3/3] Iniciando ngrok...
timeout /t 3 /nobreak > nul
start "ngrok Tunnel" cmd /k "ngrok http 5000"

echo.
echo ========================================
echo  Sistema iniciado com sucesso!
echo ========================================
echo.
echo  - API Flask: http://localhost:5000
echo  - ngrok: Verifique a URL na janela do ngrok
echo.
echo  Pressione qualquer tecla para fechar esta janela...
pause > nul
