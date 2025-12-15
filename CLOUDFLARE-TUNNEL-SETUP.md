# Configuração do Cloudflare Tunnel

## ✅ Vantagens do Cloudflare Tunnel

- 🆓 **100% GRÁTIS**
- 🔒 **Mais seguro** que ngrok
- 🌐 **Domínio fixo** (não muda nunca!)
- ⚡ **Rápido e confiável**
- 🛡️ **Funciona com firewall Fortinet** (geralmente sem problemas)

---

## 📋 Configuração Inicial (Faz UMA VEZ apenas)

### Passo 1: Criar conta Cloudflare (5 minutos)

1. Acesse: https://dash.cloudflare.com/sign-up
2. Crie uma conta gratuita (pode usar email pessoal ou da empresa)
3. Confirme o email
4. Faça login no dashboard: https://dash.cloudflare.com

### Passo 2: Baixar o cloudflared (2 minutos)

1. Acesse: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/
2. Baixe a versão para **Windows (64-bit)**
3. Extraia o arquivo `cloudflared.exe`
4. Copie o `cloudflared.exe` para a pasta do projeto:
   ```
   C:\Users\SamueldaSilvaSantos\sistema-de-login\cloudflared.exe
   ```

**OU** use o comando abaixo no PowerShell (como administrador):

```powershell
# Baixar cloudflared automaticamente
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile "cloudflared.exe"
```

### Passo 3: Autenticar com Cloudflare (3 minutos)

Dê duplo clique no arquivo: **`configurar-cloudflare.bat`**

Isso vai:
1. Abrir o navegador para você fazer login
2. Autorizar o cloudflared a usar sua conta
3. Salvar as credenciais automaticamente

### Passo 4: Criar o Túnel (AUTOMÁTICO)

O script `iniciar-sistema-cloudflare.bat` vai criar o túnel automaticamente na primeira vez.

---

## 🚀 Como Usar (Dia a Dia)

### Para INICIAR o sistema:

**Duplo clique em:** `iniciar-sistema-cloudflare.bat`

Isso vai:
1. Iniciar a API Flask
2. Criar/conectar ao túnel Cloudflare
3. Mostrar a URL pública (que NUNCA muda!)

### Para PARAR o sistema:

**Duplo clique em:** `parar-sistema.bat` (mesmo script de antes)

---

## 📝 Primeira Vez - Passo a Passo Completo

1. ✅ Criar conta Cloudflare (https://dash.cloudflare.com/sign-up)
2. ✅ Baixar `cloudflared.exe` e colocar na pasta do projeto
3. ✅ Duplo clique em `configurar-cloudflare.bat`
4. ✅ Fazer login no navegador quando abrir
5. ✅ Duplo clique em `iniciar-sistema-cloudflare.bat`
6. ✅ Copiar a URL que aparecer (ex: `https://seu-app.trycloudflare.com`)
7. ✅ Configurar essa URL no `.env.local` ou Vercel

---

## 🔧 Configurar URL Fixa Personalizada (Opcional)

Para ter uma URL tipo `https://faturas-vora.exemplo.com`:

1. No dashboard Cloudflare: https://one.dash.cloudflare.com/
2. Vá em **Access** > **Tunnels**
3. Clique em **Create a tunnel**
4. Escolha um nome (ex: "api-faturas")
5. Copie o token que aparecer
6. Cole o token no arquivo `.env` do backend:
   ```
   CLOUDFLARE_TUNNEL_TOKEN=seu-token-aqui
   ```
7. Use o script `iniciar-sistema-cloudflare-fixo.bat`

---

## ⚠️ Troubleshooting

### cloudflared não é reconhecido
- Certifique-se que `cloudflared.exe` está na pasta do projeto
- Ou adicione ao PATH do Windows

### Erro "You need to specify a hostname"
- Use o script `configurar-cloudflare.bat` primeiro
- Ou execute: `cloudflared tunnel login`

### Túnel não conecta
- Verifique se a API Flask está rodando (porta 5000)
- Verifique sua conexão com a internet
- Tente reiniciar o túnel

### Firewall bloqueia
- Cloudflare geralmente funciona mesmo com Fortinet
- Se não funcionar, peça ao TI para liberar `*.trycloudflare.com`

---

## 🆚 Comparação: ngrok vs Cloudflare

| Recurso | ngrok (grátis) | Cloudflare Tunnel |
|---------|----------------|-------------------|
| Custo | Grátis | Grátis |
| URL fixa | ❌ Não (ou só 1) | ✅ Sim |
| Velocidade | Boa | Excelente |
| Segurança | Boa | Excelente |
| Funciona com Fortinet | ⚠️ Precisa certificado | ✅ Geralmente sim |
| Limite de banda | 1GB/mês | Ilimitado |
| Configuração | Simples | Simples |

---

## 📞 Próximos Passos

1. Siga os passos acima
2. Teste o sistema
3. Se funcionar, pode desinstalar o ngrok!

Qualquer dúvida, consulte a documentação oficial:
https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
