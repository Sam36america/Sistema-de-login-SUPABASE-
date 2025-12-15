# Scripts de Automação do Sistema

## 🚀 Como Usar

### Modo 1: Sistema LOCAL (sem ngrok - para testes)
1. Dê duplo clique no arquivo **`iniciar-sistema-local.bat`**
2. Aguarde as janelas abrirem (API + Frontend)
3. Acesse: http://localhost:3000
4. ✅ Não precisa de ngrok nem certificado Fortinet!
5. ⚠️ Funciona apenas no seu computador

### Modo 2: Sistema COMPLETO Automático 🚀 MAIS FÁCIL
1. **Duplo clique em:** **`iniciar-tudo-automatico.bat`**
2. Aguarde ~30 segundos
3. Acesse: http://localhost:3000
4. ✅ Tudo é configurado automaticamente!
5. ✅ Backend + Cloudflare + Frontend iniciam sozinhos
6. ✅ .env.local atualizado automaticamente

### Modo 3: Sistema PÚBLICO com Cloudflare (manual)
1. **Primeira vez**: Execute **`configurar-cloudflare.bat`** (só uma vez)
2. **Uso diário**: Duplo clique em **`iniciar-sistema-cloudflare.bat`**
3. Copie a URL que aparecer e atualize .env.local manualmente
4. ✅ Funciona com firewall Fortinet
5. ✅ Grátis e sem limites
6. 📖 Veja: [CLOUDFLARE-TUNNEL-SETUP.md](CLOUDFLARE-TUNNEL-SETUP.md)

### Modo 4: Sistema PÚBLICO (com ngrok - alternativa)
1. Dê duplo clique no arquivo **`iniciar-sistema.bat`**
2. Aguarde as 3 janelas abrirem:
   - Janela 1: API Flask
   - Janela 2: ngrok
   - Janela 3: Confirmação (pode fechar)
3. ⚠️ Requer certificado Fortinet instalado

### Para PARAR o sistema:
1. Dê duplo clique no arquivo **`parar-sistema.bat`**
2. Confirme que tudo foi fechado

---

## 📋 O que cada script faz

### `iniciar-sistema-local.bat` ⭐ RECOMENDADO PARA COMEÇAR
✅ Inicia API Flask em http://localhost:5000
✅ Inicia Frontend Next.js em http://localhost:3000
✅ Tudo funciona localmente (sem internet)
✅ Não precisa de ngrok nem certificado Fortinet
⚠️ Acesso apenas no seu computador

### `configurar-cloudflare.bat` ⭐ NOVO!
✅ Configura Cloudflare Tunnel (só roda 1 vez)
✅ Faz login na conta Cloudflare
✅ Autoriza o túnel
⚠️ Necessário antes de usar `iniciar-sistema-cloudflare.bat`

### `iniciar-tudo-automatico.bat` 🚀 SUPER RECOMENDADO!
✅ Inicia TUDO automaticamente (Backend + Cloudflare + Frontend)
✅ Atualiza .env.local automaticamente com a URL do Cloudflare
✅ Baixa cloudflared automaticamente se não tiver
✅ Funciona com firewall Fortinet
✅ É só dar duplo clique e usar!

### `iniciar-sistema-cloudflare-auto.bat`
✅ Inicia API Flask + Cloudflare Tunnel
✅ Atualiza .env.local automaticamente
✅ Captura URL do túnel automaticamente
✅ Você precisa rodar o frontend manualmente depois

### `iniciar-sistema-cloudflare.bat`
✅ Inicia API Flask em http://localhost:5000
✅ Inicia Cloudflare Tunnel
✅ Funciona com firewall Fortinet
⚠️ Você precisa copiar URL e atualizar .env.local manualmente

### `iniciar-sistema.bat` (alternativa com ngrok)
✅ Ativa o ambiente virtual Python
✅ Inicia a API Flask em http://localhost:5000
✅ Inicia o ngrok e expõe a API publicamente
✅ Abre tudo em janelas separadas para fácil monitoramento
⚠️ Requer certificado Fortinet para funcionar

### `parar-sistema.bat`
✅ Fecha a API Flask (libera porta 5000)
✅ Fecha o Frontend Next.js (porta 3000)
✅ Fecha o ngrok
✅ Fecha o Cloudflare Tunnel
✅ Limpa todos os processos relacionados

---

## ⚠️ IMPORTANTE: URL do ngrok

**A URL do ngrok muda toda vez que você reinicia!**

Depois de rodar `iniciar-sistema.bat`:

1. Olhe na janela do **ngrok**
2. Copie a URL que aparece (tipo: `https://abc123.ngrok.io`)
3. Se estiver testando localmente:
   - Crie/edite o arquivo `.env.local` na raiz do projeto
   - Adicione: `NEXT_PUBLIC_API_URL=https://abc123.ngrok.io`
4. Se o frontend está na Vercel:
   - Vá em Settings > Environment Variables
   - Atualize `NEXT_PUBLIC_API_URL` com a nova URL
   - Faça redeploy

---

## 💡 Dicas

### Criar atalho na Área de Trabalho
1. Clique com botão direito em `iniciar-sistema.bat`
2. Escolha "Criar atalho"
3. Arraste o atalho para a Área de Trabalho
4. (Opcional) Clique direito > Propriedades > Alterar ícone

### Executar como Administrador (se necessário)
1. Clique direito em `iniciar-sistema.bat`
2. Escolha "Executar como administrador"

### Ver logs da API
- Deixe a janela "API Flask" aberta
- Todos os logs de requisições aparecem lá em tempo real

### Verificar se está rodando
Abra o navegador e acesse:
- API: http://localhost:5000
- ngrok Dashboard: http://localhost:4040

---

## 🔧 Solução de Problemas

### "venv não encontrado"
- Você precisa criar o ambiente virtual primeiro:
  ```bash
  cd backend-flask
  python -m venv venv
  pip install -r requirements.txt
  ```

### "ngrok não é reconhecido"
- Baixe o ngrok: https://ngrok.com/download
- Extraia e coloque o `ngrok.exe` em uma pasta no PATH
- Ou coloque na raiz do projeto

### Porta 5000 já está em uso
1. Execute `parar-sistema.bat`
2. Ou manualmente: `netstat -ano | findstr :5000` e mate o processo

### API não conecta ao banco
- Verifique o arquivo `backend-flask\.env`
- Confirme que o MySQL está rodando
- Teste a conexão no HeidiSQL

---

## 📞 Próximos Passos

Para **eliminar a mudança de URL** toda vez:
- Configure ngrok com domínio fixo (plano grátis tem 1 domínio!)
- Ou use Cloudflare Tunnel (100% grátis, domínio fixo)

Quer que eu te ajude com isso?
