# 🎯 lil_ken_ceo - AI CEO Agent

Виртуальный CEO для управления онлайн гемблинг бизнесом.

## 🚀 Быстрый старт

### Требования
- Python 3.9+
- Docker и Docker Compose (опционально)
- Telegram Bot Token
- Claude API Key

### 🏠 Запуск локально

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/lilagentsbet.git
cd lilagentsbet
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Скопируйте и настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env и добавьте ваши ключи
```

5. Проверьте конфигурацию:
```bash
python scripts/test_env.py
```

6. Запустите бота:
```bash
python src/main.py
```

### ☁️ Запуск через GitHub Actions

1. Настройте секреты в вашем GitHub репозитории:
   - Перейдите в Settings → Secrets and variables → Actions
   - Добавьте следующие секреты:

   **Обязательные:**
   - `TELEGRAM_BOT_TOKEN` - токен вашего Telegram бота
   - `ANTHROPIC_API_KEY` - API ключ Claude/Anthropic

   **Опциональные:**
   - `TELEGRAM_ADMIN_ID` - ваш Telegram ID для администрирования
   - `OPENAI_API_KEY` - API ключ OpenAI (если используете)

2. Push код в ветку `main` или `master`:
```bash
git push origin main
```

3. Бот автоматически запустится через GitHub Actions и будет работать в облаке!

### 🔧 Настройка секретов GitHub

Для работы бота в GitHub Actions необходимо настроить следующие секреты:

| Секрет | Описание | Обязательный |
|--------|----------|--------------|
| `TELEGRAM_BOT_TOKEN` | Токен от @BotFather | ✅ |
| `ANTHROPIC_API_KEY` | API ключ Claude | ✅ |
| `TELEGRAM_ADMIN_ID` | Ваш Telegram ID | ⚠️ |
| `OPENAI_API_KEY` | API ключ OpenAI | ⚠️ |

**Как получить секреты:**
1. `TELEGRAM_BOT_TOKEN`: Создайте бота через @BotFather в Telegram
2. `ANTHROPIC_API_KEY`: Получите на https://console.anthropic.com/
3. `TELEGRAM_ADMIN_ID`: Напишите @userinfobot в Telegram
4. `OPENAI_API_KEY`: Получите на https://platform.openai.com/

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