# 🚀 DEPLOY NA VERCEL - 3 MINUTOS

## Passo 1: Instalar Vercel CLI (opcional)
```bash
npm install -g vercel
```

## Passo 2: Subir pro GitHub
```bash
git add .
git commit -m "Configurado para Vercel"
git push origin main
```

## Passo 3: Deploy na Vercel

### Opção A - Pelo Site (MAIS FÁCIL):
1. Acesse: https://vercel.com
2. Clique em "Sign Up" e faça login com GitHub
3. Clique em "Add New Project"
4. Selecione o repositório "Sistema-Analise-Financeira"
5. Configure:
   - **Framework Preset:** Other
   - **Root Directory:** `Sistema-Analise-Financeira`
   - **Build Command:** (deixe vazio)
   - **Output Directory:** (deixe vazio)
6. Em "Environment Variables", adicione:
   - **Name:** `TWELVE_API_KEY`
   - **Value:** `sua_chave_api_aqui`
7. Clique em "Deploy"

### Opção B - Pelo Terminal:
```bash
cd Sistema-Analise-Financeira
vercel
```

## ✅ Pronto!
Seu app estará em:
```
https://sistema-analise-financeira.vercel.app
```

## 📌 Vantagens da Vercel:
- ✅ Deploy em 30 segundos
- ✅ Não dorme (sempre ativo!)
- ✅ SSL automático
- ✅ URL profissional
- ✅ 100% grátis
- ✅ Perfeito para portfólio

## 🔄 Atualizações Automáticas:
Toda vez que você fizer `git push`, a Vercel atualiza automaticamente!

## ⚠️ Observação:
Se der erro de timeout, é porque o plano grátis tem limite de 10 segundos por requisição. Para portfólio funciona perfeitamente!
