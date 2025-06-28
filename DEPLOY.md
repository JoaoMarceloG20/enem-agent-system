# Guia de Deploy - ENEM Agent System

## 🎯 Pré-requisitos

### Para GCP (Backend)
- Conta no Google Cloud Platform
- `gcloud` CLI instalado e configurado
- Projeto GCP criado
- APIs habilitadas: App Engine, Cloud Build, Cloud Run

### Para Vercel (Frontend)
- Conta na Vercel
- `vercel` CLI instalado
- Repositório GitHub (opcional)

## 🚀 Deploy do Backend (GCP)

### Opção 1: App Engine (Recomendado)

1. **Configure o projeto GCP:**
```bash
gcloud config set project SEU_PROJECT_ID
gcloud app create --region=us-central
```

2. **Configure as variáveis de ambiente:**
```bash
# Edite o arquivo app.yaml com suas credenciais
GOOGLE_API_KEY=sua_chave_gemini
POSTGRES_URL=sua_url_postgres
REDIS_URL=sua_url_redis
QDRANT_URL=sua_url_qdrant
```

3. **Deploy:**
```bash
gcloud app deploy app.yaml
```

### Opção 2: Cloud Run

1. **Configure variáveis no Cloud Build:**
```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_GOOGLE_API_KEY=sua_chave,_POSTGRES_URL=sua_url_postgres,_REDIS_URL=sua_url_redis,_QDRANT_URL=sua_url_qdrant
```

## 🌐 Deploy do Frontend (Vercel)

### Opção 1: Via CLI

1. **Instale as dependências:**
```bash
cd frontend
npm install
```

2. **Configure a variável de ambiente:**
```bash
# No dashboard da Vercel, adicione:
NEXT_PUBLIC_API_URL=https://SEU_BACKEND_URL
```

3. **Deploy:**
```bash
vercel --prod
```

### Opção 2: Via GitHub (Recomendado)

1. **Push para GitHub:**
```bash
git add .
git commit -m "Add frontend"
git push origin main
```

2. **Conecte na Vercel:**
- Vá para vercel.com
- Importe o repositório
- Configure `root directory` como `frontend`
- Adicione variável: `NEXT_PUBLIC_API_URL`

## 🔧 Configuração de Infraestrutura

### Banco de Dados (PostgreSQL)
```bash
# Google Cloud SQL
gcloud sql instances create enem-postgres \
  --database-version=POSTGRES_13 \
  --region=us-central1 \
  --tier=db-f1-micro
```

### Redis
```bash
# Google Cloud Memorystore
gcloud redis instances create enem-redis \
  --region=us-central1 \
  --size=1
```

### Qdrant (Vector Database)
```bash
# Deploy no Google Cloud Run
gcloud run deploy qdrant \
  --image=qdrant/qdrant:latest \
  --platform=managed \
  --region=us-central1 \
  --port=6333
```

## 🛡️ Configuração de Segurança

### CORS no Backend
```python
# Adicione no main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Variáveis de Ambiente
```bash
# .env (local)
GOOGLE_API_KEY=sua_chave
POSTGRES_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://host:6379
QDRANT_URL=https://host:6333

# GCP App Engine (app.yaml)
env_variables:
  GOOGLE_API_KEY: ${GOOGLE_API_KEY}
  
# Vercel (dashboard)
NEXT_PUBLIC_API_URL=https://seu-backend.appspot.com
```

## 📊 Monitoramento

### Logs do Backend
```bash
# App Engine
gcloud app logs tail -s default

# Cloud Run
gcloud logging read "resource.type=cloud_run_revision"
```

### Métricas
- Google Cloud Monitoring
- Vercel Analytics
- Logs estruturados no FastAPI

## 🔄 CI/CD (Opcional)

### GitHub Actions para Backend
```yaml
# .github/workflows/deploy-backend.yml
name: Deploy Backend
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/setup-gcloud@v0
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      - run: gcloud app deploy app.yaml --quiet
```

## 🆘 Troubleshooting

### Problemas Comuns

1. **Timeout no deploy:**
```bash
gcloud config set app/cloud_build_timeout 1200
```

2. **Erro de CORS:**
- Verifique origins no middleware
- Configure domínio correto

3. **Variáveis de ambiente:**
- Confirme configuração no dashboard
- Verifique sintaxe nos arquivos

4. **Dependências Python:**
```bash
pip freeze > requirements.txt
```

### Comandos Úteis

```bash
# Verificar status
gcloud app describe
vercel ls

# Logs em tempo real
gcloud app logs tail -s default
vercel logs SEU_DEPLOYMENT_URL

# Rollback
gcloud app versions stop VERSION_ID
vercel rollback SEU_DEPLOYMENT_URL
```

## 💰 Custos Estimados

### GCP (Backend)
- App Engine: ~$20-50/mês
- Cloud SQL: ~$15-30/mês
- Cloud Run: ~$10-25/mês (pay-per-use)

### Vercel (Frontend)
- Pro Plan: $20/mês (recomendado)
- Hobby: Gratuito (limitado)

## 🎉 Checklist Final

- [ ] Backend funcionando localmente
- [ ] Frontend funcionando localmente
- [ ] Variáveis de ambiente configuradas
- [ ] Infraestrutura GCP criada
- [ ] Deploy do backend realizado
- [ ] Deploy do frontend realizado
- [ ] CORS configurado
- [ ] Teste end-to-end funcionando
- [ ] Monitoramento configurado
- [ ] Domínio personalizado (opcional)

---

**Sucesso! Seu ENEM Agent System está online! 🚀**