# Deploy para Vercel - Sistema de Leitura de Faturas

## O que será hospedado na Vercel?

✅ **Frontend Next.js** (interface web, autenticação Supabase)
❌ **Backend Flask NÃO** (APIs de processamento)

O backend Flask precisa ser hospedado separadamente ou usar Cloudflare Tunnel local.

---

## Passo 1: Instalar Vercel CLI (Opcional)

```bash
npm install -g vercel
```

---

## Passo 2: Deploy via GitHub (RECOMENDADO)

### 2.1. Acesse a Vercel
1. Acesse: https://vercel.com
2. Faça login com sua conta GitHub
3. Clique em "Add New Project"

### 2.2. Importar Repositório
1. Selecione o repositório: `Sam36america/Sistema-de-login-SUPABASE-`
2. Clique em "Import"

### 2.3. Configurar Projeto
- **Framework Preset**: Next.js (detectado automaticamente)
- **Root Directory**: `.` (deixe padrão)
- **Build Command**: `npm run build` (padrão)
- **Output Directory**: `.next` (padrão)

### 2.4. Configurar Variáveis de Ambiente

⚠️ **CRÍTICO**: Adicione estas variáveis na seção "Environment Variables":

```env
NEXT_PUBLIC_SUPABASE_URL=https://nputagdeoxjzuuzciwih.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5wdXRhZ2Rlb3hqenV1emNpd2loIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUxOTEyOTIsImV4cCI6MjA4MDc2NzI5Mn0.SDOcj9PdRBNpkhXgl9ORDmiMxEeF24o7HoSjhp4vUH8
TURBOPACK=0
NEXT_PUBLIC_API_URL=https://SUA-URL-CLOUDFLARE.trycloudflare.com
```

⚠️ **ATENÇÃO**: Substitua `NEXT_PUBLIC_API_URL` pela URL do seu backend:
- Se usar **Cloudflare Tunnel local**: Coloque a URL que aparece quando roda `iniciar-tudo-automatico.bat`
- Se hospedar o backend: Coloque a URL do serviço hospedado

### 2.5. Deploy
1. Clique em "Deploy"
2. Aguarde ~2-3 minutos
3. Vercel vai gerar uma URL tipo: `https://sistema-de-login-supabase.vercel.app`

---

## Passo 3: Configurar Backend (APIs)

Você tem 3 opções:

### Opção A: Cloudflare Tunnel Local (Atual)
✅ **Vantagem**: Grátis, rápido de configurar
❌ **Desvantagem**: Precisa rodar localmente, URL muda sempre

1. Rode `iniciar-tudo-automatico.bat` (já faz tudo)
2. Copie a URL do Cloudflare que aparece (ex: `https://abc-123.trycloudflare.com`)
3. Na Vercel, vá em **Settings → Environment Variables**
4. Edite `NEXT_PUBLIC_API_URL` com a nova URL
5. Vá em **Deployments** → Clique nos 3 pontinhos → "Redeploy"

⚠️ **Problema**: A URL muda toda vez que reinicia! Precisa atualizar na Vercel sempre.

**Solução**: Use Cloudflare Tunnel com domínio fixo (requer domínio próprio) ou hospede o backend.

---

### Opção B: Railway (Hospedar Backend Flask)
✅ **Vantagem**: URL fixa, grátis (trial $5), sempre online
❌ **Desvantagem**: Precisa migrar o código

**Passos rápidos**:
1. Acesse https://railway.app
2. Login com GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Selecione o repositório
5. Configure variáveis de ambiente do banco SQL
6. Railway vai gerar URL fixa: `https://seu-app.railway.app`
7. Atualize `NEXT_PUBLIC_API_URL` na Vercel com essa URL

**Necessário**: Criar `Procfile` e `requirements.txt` na pasta `backend-flask`

---

### Opção C: Render (Hospedar Backend Flask)
✅ **Vantagem**: URL fixa, grátis (plano free), sempre online
❌ **Desvantagem**: Mais lento que Railway

Similar ao Railway, mas usando https://render.com

---

## Passo 4: Testar Deploy

1. Acesse a URL da Vercel (ex: `https://sistema-de-login-supabase.vercel.app`)
2. Teste login/cadastro (Supabase funciona direto)
3. Teste dashboard:
   - **SE backend estiver rodando**: Fornecedoras devem aparecer
   - **SE backend estiver offline**: Vai ficar "Carregando fornecedoras..."

---

## Passo 5: Domínio Personalizado (Opcional)

Na Vercel:
1. Vá em **Settings → Domains**
2. Adicione seu domínio (ex: `leitura-faturas.voraenergia.com.br`)
3. Configure DNS conforme instruções da Vercel

---

## Deploy via CLI (Alternativa)

Se preferir linha de comando:

```bash
# Login na Vercel
vercel login

# Fazer deploy
vercel

# Deploy para produção
vercel --prod
```

A CLI vai perguntar as mesmas configurações.

---

## Atualizações Automáticas

✅ A Vercel detecta automaticamente commits na branch `main`
✅ Toda vez que você fizer `git push`, a Vercel faz deploy automático

Para desabilitar deploy automático:
1. Vercel → Settings → Git
2. Desmarque "Production Branch"

---

## Problemas Comuns

### 1. "Carregando fornecedoras..." infinito
**Causa**: Backend offline ou URL errada no `NEXT_PUBLIC_API_URL`
**Solução**:
- Verifique se backend está rodando
- Confirme URL correta nas variáveis de ambiente
- Redeploy na Vercel

### 2. Erro de CORS
**Causa**: Backend não aceita requisições da URL da Vercel
**Solução**: No `backend-flask/app.py`, já está configurado `origins: "*"` (aceita tudo)

### 3. Erro 404 ao acessar rotas
**Causa**: Next.js routing
**Solução**: Já está configurado corretamente (app router)

### 4. Build falha na Vercel
**Causa**: Erro de TypeScript ou dependências
**Solução**: Rode `npm run build` localmente primeiro para testar

---

## Estrutura Final

```
Internet
   │
   ├─► Frontend (Vercel)
   │   └─► https://sistema-de-login-supabase.vercel.app
   │
   ├─► Autenticação (Supabase)
   │   └─► https://nputagdeoxjzuuzciwih.supabase.co
   │
   └─► Backend Flask (Railway/Render/Local+Cloudflare)
       └─► https://sua-api-url.com
```

---

## Próximos Passos

1. ✅ Deploy frontend na Vercel
2. ⚠️ Decidir onde hospedar backend (Railway, Render ou manter local)
3. ⚠️ Configurar `NEXT_PUBLIC_API_URL` com URL fixa do backend
4. ✅ Testar sistema completo

---

## Precisa de Ajuda?

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Deploy**: https://nextjs.org/docs/deployment
- **Railway**: https://docs.railway.app
- **Render**: https://render.com/docs
