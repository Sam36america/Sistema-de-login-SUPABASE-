# Backend Flask - API de Leitura de Faturas

API Flask para processar faturas de gás em PDF e XML, extrair informações e armazenar no banco de dados MySQL.

## Características

- Upload de arquivos PDF e XML
- Extração automática de dados das faturas
- Validação de duplicatas
- Armazenamento em MySQL
- API RESTful para integração com frontend Next.js
- CORS configurado para comunicação cross-origin

## Pré-requisitos

- Python 3.8 ou superior
- MySQL ODBC Driver 8.0
- Acesso ao banco de dados MySQL da empresa
- Acesso à rede interna (para processar arquivos de rede)

## Instalação

### 1. Instalar Python (se necessário)

Baixe e instale Python 3.8+ de: https://www.python.org/downloads/

### 2. Criar ambiente virtual

```bash
cd backend-flask
python -m venv venv
```

### 3. Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
copy .env.example .env
```

Edite o arquivo `.env` com suas configurações.

### 6. Instalar MySQL ODBC Driver

Se ainda não tiver instalado:

**Windows:**
- Baixe de: https://dev.mysql.com/downloads/connector/odbc/
- Instale o "MySQL Connector/ODBC 8.0"

**Linux:**
```bash
sudo apt-get install unixodbc unixodbc-dev
sudo apt-get install libmyodbc
```

## Executar a API

```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

## Endpoints da API

### Health Check
```
GET /api/health
```

Verifica se a API e banco de dados estão funcionando.

### Upload de Arquivo
```
POST /api/upload
Content-Type: multipart/form-data

Body:
- file: arquivo PDF ou XML
```

Envia um arquivo para processamento.

### Processar Fatura
```
POST /api/processar
Content-Type: application/json

Body:
{
  "filepath": "caminho/do/arquivo.pdf"
}
```

Processa um arquivo já enviado.

### Listar Faturas
```
GET /api/faturas
```

Retorna as últimas 50 faturas processadas.

### Listar Clientes
```
GET /api/clientes
```

Retorna lista de clientes cadastrados.

### Listar Fornecedores
```
GET /api/fornecedores
```

Retorna lista de fornecedores cadastrados.

## Estrutura do Projeto

```
backend-flask/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── .env                   # Configurações (não commitado)
├── .env.example          # Exemplo de configurações
├── scripts/              # Scripts de processamento
│   ├── main_sql.py       # Script principal
│   ├── functions.py      # Funções de extração
│   ├── sql_functions.py  # Funções de banco de dados
│   ├── models.py         # Modelos e configurações
│   └── config.py         # Configurações gerais
├── uploads/              # Arquivos enviados
└── temp/                 # Arquivos temporários
```

## Usar com ngrok (Expor API para internet)

Para que o frontend na Vercel acesse a API local:

### 1. Instalar ngrok

Baixe de: https://ngrok.com/download

### 2. Executar ngrok

```bash
ngrok http 5000
```

### 3. Copiar URL pública

Ngrok fornecerá uma URL como: `https://abc123.ngrok.io`

### 4. Atualizar frontend

No frontend Next.js, configure a API_URL com a URL do ngrok.

## Troubleshooting

### Erro: "MySQL ODBC Driver not found"

Instale o MySQL Connector/ODBC 8.0.

### Erro: "Connection refused"

Verifique se:
- A API está rodando
- A porta 5000 está liberada no firewall
- As credenciais do banco estão corretas no `.env`

### Erro: "CORS blocked"

Verifique se `flask-cors` está instalado e configurado no `app.py`.

## Desenvolvimento

Para rodar em modo debug:

```bash
set FLASK_ENV=development
set FLASK_DEBUG=1
python app.py
```

## Produção

Para produção, use um servidor WSGI como Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Segurança

- Nunca commite o arquivo `.env` com credenciais
- Use HTTPS em produção (ngrok fornece automaticamente)
- Implemente autenticação JWT se necessário
- Valide todos os inputs
- Limite tamanho de upload de arquivos

## Suporte

Para dúvidas ou problemas, entre em contato com o time de desenvolvimento.
