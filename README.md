# Sistema de Login com Supabase e Next.js

Sistema completo de autenticação usando Supabase, Next.js 15, TypeScript e Tailwind CSS.

## Funcionalidades

- Cadastro de usuários
- Login com email e senha
- Logout
- Proteção de rotas
- Página dashboard protegida
- Middleware de autenticação automática

## Configuração

### 1. Configurar o Supabase

1. Acesse [https://app.supabase.com](https://app.supabase.com)
2. Crie um novo projeto ou selecione um existente
3. Vá em **Settings** > **API**
4. Copie as seguintes informações:
   - **Project URL** (algo como: https://xxxxx.supabase.co)
   - **anon public** key

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env.local` na raiz do projeto e adicione suas credenciais:

```env
NEXT_PUBLIC_SUPABASE_URL=sua-url-do-projeto
NEXT_PUBLIC_SUPABASE_ANON_KEY=sua-chave-anon
```

### 3. Configurar Autenticação no Supabase

1. No painel do Supabase, vá em **Authentication** > **Providers**
2. Certifique-se de que **Email** está habilitado
3. Em **Authentication** > **URL Configuration**, adicione:
   - **Site URL**: `http://localhost:3000` (desenvolvimento)
   - **Redirect URLs**: `http://localhost:3000/auth/callback`

### 4. Instalar Dependências

```bash
npm install
```

### 5. Executar o Projeto

```bash
npm run dev
```

O projeto estará disponível em [http://localhost:3000](http://localhost:3000)

## Estrutura do Projeto

```
sistema-de-login/
├── app/
│   ├── auth/
│   │   └── callback/
│   │       └── route.ts          # Callback de autenticação
│   ├── dashboard/
│   │   └── page.tsx              # Página protegida
│   ├── login/
│   │   └── page.tsx              # Página de login
│   ├── signup/
│   │   └── page.tsx              # Página de cadastro
│   └── page.tsx                  # Página inicial (redireciona)
├── components/
│   └── LogoutButton.tsx          # Componente de logout
├── lib/
│   └── supabase/
│       ├── client.ts             # Cliente Supabase (browser)
│       ├── server.ts             # Cliente Supabase (server)
│       └── middleware.ts         # Configuração do middleware
├── middleware.ts                 # Middleware de proteção de rotas
└── .env.local                    # Variáveis de ambiente
```

## Como Usar

### Cadastro

1. Acesse `/signup`
2. Preencha email e senha (mínimo 6 caracteres)
3. Verifique seu email para confirmar a conta (se configurado no Supabase)
4. Faça login em `/login`

### Login

1. Acesse `/login`
2. Preencha suas credenciais
3. Você será redirecionado para `/dashboard`

### Dashboard

- Área protegida que só pode ser acessada por usuários autenticados
- Exibe informações do usuário logado
- Botão de logout

## Proteção de Rotas

O middleware protege automaticamente todas as rotas exceto:
- `/login`
- `/signup`
- Arquivos estáticos

Usuários não autenticados são redirecionados para `/login`.

## Tecnologias Utilizadas

- **Next.js 15** - Framework React com App Router
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Supabase** - Backend e autenticação
- **@supabase/ssr** - Integração Supabase com SSR

## Próximos Passos

Agora que o sistema de autenticação está funcionando, você pode:

1. Adicionar recuperação de senha
2. Criar perfil de usuário
3. Adicionar autenticação social (Google, GitHub, etc.)
4. Desenvolver as páginas do seu site
5. Adicionar roles e permissões

## Solução de Problemas

### Erro: "Invalid API key"

- Verifique se as variáveis de ambiente em `.env.local` estão corretas
- Reinicie o servidor de desenvolvimento após alterar `.env.local`

### Erro: "Email not confirmed"

- Por padrão, o Supabase requer confirmação de email
- Desabilite em: **Authentication** > **Settings** > desmarque "Enable email confirmations"

### Redirecionamento não funciona

- Verifique as URLs de redirecionamento no painel do Supabase
- Certifique-se de que `http://localhost:3000/auth/callback` está nas Redirect URLs
