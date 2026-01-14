# 🚀 DEPLOY NO RENDER - GUIA RÁPIDO

## Passo 1: Preparar GitHub
```bash
git add .
git commit -m "Preparado para deploy no Render"
git push origin main
```

## Passo 2: Criar conta no Render
1. Acesse: https://render.com
2. Clique em "Get Started for Free"
3. Faça login com GitHub

## Passo 3: Criar Web Service
1. No dashboard, clique em "New +"
2. Selecione "Web Service"
3. Conecte seu repositório GitHub
4. Selecione o repositório "Sistema-Analise-Financeira"

## Passo 4: Configurar o Deploy
Preencha os campos:

- **Name:** `sistema-analise-financeira` (ou qualquer nome)
- **Region:** `Frankfurt (EU Central)` ou `Oregon (US West)`
- **Branch:** `main`
- **Root Directory:** `Sistema-Analise-Financeira`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app_simples:app --bind 0.0.0.0:$PORT`

## Passo 5: Adicionar Variáveis de Ambiente
Na seção "Environment Variables", adicione:

- **Key:** `TWELVE_API_KEY`
- **Value:** `sua_chave_api_aqui`

Clique em "Add"

## Passo 6: Deploy
1. Selecione o plano **FREE**
2. Clique em "Create Web Service"
3. Aguarde 5-10 minutos (primeira vez demora mais)

## ✅ Pronto!
Seu app estará disponível em:
```
https://sistema-analise-financeira.onrender.com
```

## 📌 Para colocar no Portfólio/LinkedIn:

**Título:** Sistema de Análise Financeira com Machine Learning

**Descrição:**
Dashboard interativo para análise técnica de ações com 10+ indicadores e previsões usando ML. Desenvolvido com Python, Flask, Pandas, Scikit-learn e Plotly.

**Link:** https://seu-app.onrender.com

**GitHub:** https://github.com/seu-usuario/sistema-analise-financeira

**Stack:** Python | Flask | Pandas | Scikit-learn | Plotly | REST API

---

## ⚠️ Observações:
- App dorme após 15min sem uso (plano grátis)
- Primeira requisição após dormir leva ~30s
- Para portfólio isso é PERFEITO (recrutadores não ligam)
- Se quiser que fique sempre ativo, use serviço como UptimeRobot (grátis) para fazer ping a cada 5min
