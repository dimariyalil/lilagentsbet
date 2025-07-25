# 🎯 lil_ken_ceo - AI CEO Agent

Виртуальный CEO для управления онлайн гемблинг бизнесом.

## 🚀 Быстрый старт

### Требования
- Python 3.9+
- Docker и Docker Compose
- Telegram Bot Token
- Claude API Key

### Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/lilagentsbet.git
cd lilagentsbet
```

2. Скопируйте и настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши ключи
```

3. Запустите Docker контейнеры:
```bash
docker-compose up -d
```

4. Установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

5. Запустите бота:
```bash
python src/main.py
```

## 📋 Доступные команды

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/yearstrategy` - Генерация годовой стратегии
- `/marketanalysis [страна]` - Анализ нового рынка
- `/competitorwatch` - Мониторинг конкурентов
- `/swotanalysis` - SWOT анализ компании
- `/riskassessment` - Оценка бизнес-рисков
- `/dailyreport` - Ежедневный отчет
- `/weeklyreport` - Еженедельный отчет
- `/status` - Статус системы

## 🏗️ Архитектура

```
├── Telegram Bot (интерфейс)
├── CEO Agent (бизнес-логика)
├── Claude AI (искусственный интеллект)
├── ChromaDB (база знаний)
├── Redis (кратковременная память)
├── PostgreSQL (долговременное хранение)
└── n8n (автоматизация)
```

## 📚 База знаний

Добавьте документы в `data/knowledge_base/lil_ken_ceo/`:
- Стратегические планы
- Финансовые отчеты
- Анализы рынков
- Данные о конкурентах

## 🔧 Разработка

### Запуск тестов:
```bash
pytest tests/
```

### Форматирование кода:
```bash
black src/
flake8 src/
```

### Добавление нового агента:
1. Создайте папку `src/agents/new_agent/`
2. Скопируйте структуру из `lil_ken_ceo`
3. Адаптируйте промпты и команды
4. Добавьте в конфигурацию

## 📊 Мониторинг

- Логи: `logs/`
- Метрики: http://localhost:8090/metrics
- n8n: http://localhost:5678

## 🤝 Вклад

1. Fork репозитория
2. Создайте feature branch
3. Commit изменения
4. Push в branch
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. LICENSE файл

## 📞 Поддержка

- Telegram: @your_support_bot
- Email: support@lilagents.com
- Issues: GitHub Issues

---

Built with ❤️ by lil agents team