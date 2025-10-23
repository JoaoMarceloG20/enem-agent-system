#!/bin/bash
set -e

echo "🔄 Parando containers..."
docker compose down

echo "🏗️  Rebuilding imagem backend (sem cache)..."
docker compose build --no-cache backend

echo "🚀 Iniciando containers..."
docker compose up -d

echo "✅ Rebuild completo! Aguardando containers iniciarem..."
sleep 5

echo "📋 Status dos containers:"
docker compose ps

echo ""
echo "📊 Logs do backend (últimas 20 linhas):"
docker compose logs --tail=20 backend
