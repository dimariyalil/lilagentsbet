#!/bin/bash

echo "🚀 Setting up lil_ken_ceo agent..."

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required"
    exit 1
fi

# Создание виртуального окружения
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Установка зависимостей
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Проверка .env файла
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys!"
fi

# Создание директорий
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p data/knowledge_base/lil_ken_ceo/{strategies,market_data,reports,competitors}

# Запуск Docker контейнеров
echo "🐳 Starting Docker containers..."
docker-compose up -d

# Ожидание запуска
echo "⏳ Waiting for services to start..."
sleep 10

# Проверка сервисов
echo "✅ Checking services..."
docker-compose ps

echo "✨ Setup complete!"
echo "🚀 Run 'python src/main.py' to start the bot"