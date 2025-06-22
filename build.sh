#!/usr/bin/env bash
# exit on error
set -o errexit

echo "--- Iniciando o script de build ---"

echo "Passo 1: Instalando dependências do sistema para WeasyPrint..."
apt-get update && apt-get install -y libpango-1.0-0 libpangoft2-1.0-0

echo "Passo 2: Instalando dependências do Python..."
pip install -r requirements.txt

echo "Passo 3: Rodando migrações do banco de dados..."
alembic upgrade head

echo "--- Script de build concluído com sucesso ---"