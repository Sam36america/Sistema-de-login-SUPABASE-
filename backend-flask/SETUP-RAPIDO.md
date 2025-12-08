# Setup Rápido - Backend Flask

## Primeira Vez (Setup Inicial)

### Passo 1: Instalar Python
- Baixe Python 3.8+: https://www.python.org/downloads/
- Durante instalação, marque "Add Python to PATH"

### Passo 2: Instalar MySQL ODBC Driver
- Baixe: https://dev.mysql.com/downloads/connector/odbc/
- Instale "MySQL Connector/ODBC 8.0 Unicode Driver"

### Passo 3: Criar Ambiente Virtual
```bash
cd backend-flask
python -m venv venv
```

### Passo 4: Ativar Ambiente e Instalar Dependências
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Passo 5: Configurar Variáveis de Ambiente
```bash
copy .env.example .env
```
Edite o `.env` se necessário (credenciais do banco já estão configuradas)

---

## Toda Vez que For Usar

### Opção A: Usando o Script Automático (RECOMENDADO)
```bash
cd backend-flask
start.bat
```

### Opção B: Manual
```bash
cd backend-flask
venv\Scripts\activate
python app.py
```

---

## Expor para Internet (ngrok)

### Primeira Vez
1. Baixe ngrok: https://ngrok.com/download
2. Descompacte em uma pasta (ex: `C:\ngrok`)
3. Adicione ao PATH ou use caminho completo

### Toda Vez
```bash
# Em outro terminal (deixe a API rodando)
ngrok http 5000
```

Copie a URL que aparece (ex: `https://abc123.ngrok.io`)

---

## Testar se Está Funcionando

Abra no navegador:
- http://localhost:5000/ - Deve mostrar status da API
- http://localhost:5000/api/health - Deve mostrar "healthy"

Se ver isso, está tudo certo!

---

## Problemas Comuns

### "python não é reconhecido"
- Reinstale Python marcando "Add to PATH"
- Ou use caminho completo: `C:\Python\python.exe`

### "MySQL ODBC Driver not found"
- Instale o driver MySQL ODBC 8.0

### "Erro ao conectar ao banco"
- Verifique credenciais no `.env`
- Teste conexão com HeidiSQL primeiro

### "Porta 5000 já está em uso"
- Feche outros programas usando a porta
- Ou mude a porta no `app.py`: `app.run(port=5001)`

---

## Comandos Úteis

### Ver dependências instaladas
```bash
pip list
```

### Atualizar dependências
```bash
pip install -r requirements.txt --upgrade
```

### Desativar ambiente virtual
```bash
deactivate
```

---

## Próximos Passos

1. ✅ Rodar a API Flask (`python app.py`)
2. ✅ Testar no navegador (`http://localhost:5000`)
3. ✅ Rodar ngrok (`ngrok http 5000`)
4. ✅ Copiar URL do ngrok
5. ✅ Configurar no frontend (arquivo `.env.local`)
6. ✅ Testar upload de faturas!

---

## Dica Pro

Crie um atalho no desktop para `start.bat` para iniciar a API com um clique!
