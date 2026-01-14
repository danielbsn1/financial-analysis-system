# 🚀 DEPLOY NO RENDER - SUPER SIMPLES

## Passo 1: Subir pro GitHub
```bash
git add .
git commit -m "Deploy Render"
git push origin main
```

## Passo 2: Criar conta no Render
1. Acesse: https://render.com
2. Clique em "Get Started" 
3. Login com GitHub (GRÁTIS, sem cartão)

## Passo 3: Criar Web Service
1. No dashboard, clique em "New +"
2. Selecione "Web Service"
3. Clique em "Connect" no seu repositório
4. Configure:

**Name:** `sistema-analise-financeira`

**Root Directory:** `Sistema-Analise-Financeira`

**Build Command:** `pip install -r requirements.txt`

**Start Command:** `gunicorn app_simples:app`

**Instance Type:** `Free`

## Passo 4: Variável de Ambiente
Clique em "Advanced" e adicione:

**Key:** `TWELVE_API_KEY`
**Value:** `sua_chave_api_twelvedata`

## Passo 5: Deploy
Clique em "Create Web Service"

Aguarde 5 minutos (primeira vez demora)

## ✅ PRONTO!
Seu app estará em: `https://sistema-analise-financeira.onrender.com`

---

## ⚠️ IMPORTANTE:
- App dorme após 15min sem uso (plano grátis)
- Primeira requisição leva ~30s para acordar
- Para portfólio isso é PERFEITO!

## 📌 Coloque no LinkedIn:
"Sistema de Análise Financeira com ML
🔗 https://seu-app.onrender.com
💻 https://github.com/danielbsn1/Sistema-Analise-Financeira"
