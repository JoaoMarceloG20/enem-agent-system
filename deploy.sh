#!/bin/bash

echo "🚀 Deploy do ENEM Agent System"

# Deploy Backend na GCP
echo "📦 Fazendo deploy do backend na GCP..."
gcloud app deploy app.yaml --quiet

# Ou usando Cloud Run
# gcloud builds submit --config cloudbuild.yaml

echo "✅ Backend deployed!"

# Deploy Frontend na Vercel
echo "🌐 Fazendo deploy do frontend na Vercel..."
cd frontend
vercel --prod

echo "✅ Deploy completo!"
echo "🎉 Sistema online!"