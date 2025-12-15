#!/bin/bash
set -e

echo "webhook" > /app/.moduleignore
echo "▶ .moduleignore creado"

echo "▶ Running migrations..."
flask db upgrade

echo "▶ Cleaning database and running seeders..."
python -m rosemary db:reset -y
python -m rosemary db:seed || echo "No seeders or already seeded"

echo "▶ Starting Flask app..."
exec flask run --host=0.0.0.0 --port=5000
