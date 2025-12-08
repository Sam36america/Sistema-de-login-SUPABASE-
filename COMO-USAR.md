# Como Usar o Sistema de Leitura de Faturas

## Visão Geral

Sistema completo de autenticação + leitura de faturas de gás com:
- **Frontend**: Next.js hospedado na Vercel
- **Backend**: Flask rodando localmente no PC da empresa
- **Banco de Dados**: MySQL (HeidiSQL)

## Configuração Rápida

### 1. Backend Flask (API Local)

```bash
cd backend-flask

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de configuração
copy .env.example .env

# Editar .env com suas configurações (se necessário)
notepad .env

# Rodar a API
python app.py
```

A API estará rodando em: `http://localhost:5000`

### 2. Expor API com ngrok

Para que o frontend na Vercel acesse sua API local:

```bash
# Baixar ngrok de: https://ngrok.com/download

# Rodar ngrok
ngrok http 5000
```

Ngrok vai te dar uma URL pública tipo: `https://abc123.ngrok.io`

### 3. Configurar Frontend

No projeto Next.js, crie um arquivo `.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://abc123.ngrok.io
```

**IMPORTANTE**: Sempre que reiniciar o ngrok, a URL muda. Você precisa atualizar o `.env.local` com a nova URL.

### 4. Testar Localmente (Opcional)

Se quiser testar tudo local antes de subir para Vercel:

```bash
# Terminal 1 - Backend Flask
cd backend-flask
python app.py

# Terminal 2 - Frontend Next.js
npm run dev
```

Acesse: `http://localhost:3000`

## Como Usar o Sistema

### 1. Fazer Login

- Acesse o sistema
- Faça login com suas credenciais (cadastradas no Supabase)

### 2. Upload de Faturas

- Na página do Dashboard, clique em "Selecione o arquivo"
- Escolha um PDF ou XML de fatura
- Clique em "Enviar e Processar"

### 3. O que Acontece

1. Arquivo é enviado para a API Flask
2. API extrai informações (CNPJ, valores, datas, etc)
3. Verifica duplicatas no banco
4. Insere no MySQL
5. Move arquivo para pasta "Lidos"
6. Atualiza a lista de faturas na tela

## Estrutura de Pastas

```
sistema-de-login/
├── app/                      # Frontend Next.js
│   ├── login/               # Página de login
│   ├── signup/              # Página de cadastro
│   └── dashboard/           # Dashboard principal
├── backend-flask/           # Backend API Flask
│   ├── app.py              # Aplicação Flask
│   ├── scripts/            # Scripts de processamento
│   ├── uploads/            # Arquivos enviados
│   └── requirements.txt    # Dependências Python
├── lib/                     # Bibliotecas
└── public/                  # Arquivos públicos (logo, etc)
```

## Endpoints da API

- `GET /` - Status da API
- `GET /api/health` - Health check
- `POST /api/upload` - Upload de arquivo
- `POST /api/processar` - Processar fatura
- `GET /api/faturas` - Listar faturas
- `GET /api/clientes` - Listar clientes
- `GET /api/fornecedores` - Listar fornecedores

## Troubleshooting

### API não conecta ao banco

Verifique as credenciais no arquivo `backend-flask/.env`

### Frontend não acessa API

1. Verifique se a API Flask está rodando: `http://localhost:5000`
2. Verifique se o ngrok está ativo
3. Verifique se a URL no `.env.local` está correta
4. Verifique CORS no `app.py`

### Erro ao processar PDF

1. Verifique se PyPDF2 está instalado
2. Verifique se o PDF não está corrompido
3. Verifique os logs da API no terminal

### Erro "MySQL ODBC Driver not found"

Instale o MySQL Connector/ODBC 8.0:
https://dev.mysql.com/downloads/connector/odbc/

## Dicas

### Manter API Rodando 24/7

Use `pm2` ou `nssm` no Windows para rodar a API como serviço:

```bash
pip install waitress

# Criar arquivo start.py
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Usar IP Fixo em vez de ngrok

Se tiver IP fixo na empresa:
1. Configure roteador para encaminhar porta 5000
2. Use o IP público no `.env.local`
3. Configure SSL com Let's Encrypt

### Logs

Logs da API aparecem no terminal onde você rodou `python app.py`

## Segurança

- Nunca commite o arquivo `.env` com credenciais
- Use HTTPS (ngrok já fornece)
- Mantenha Python e dependências atualizadas
- Limite tamanho de upload no Flask

## Suporte

Para dúvidas, entre em contato com o desenvolvedor.
