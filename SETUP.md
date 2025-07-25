# 🚀 Руководство по установке lil_ken_ceo

## Предварительные требования

### Системные требования
- **Python**: 3.9 или выше
- **Docker**: 20.10+ и Docker Compose 2.0+
- **Git**: для клонирования репозитория
- **Минимум 4GB RAM** и **10GB свободного места**

### API Ключи
Перед началом получите следующие ключи:

1. **Telegram Bot Token**
   - Напишите [@BotFather](https://t.me/botfather)
   - Создайте нового бота: `/newbot`
   - Сохраните токен

2. **Claude API Key**
   - Зарегистрируйтесь на [console.anthropic.com](https://console.anthropic.com)
   - Создайте API ключ
   - Убедитесь что у вас есть кредиты

3. **Telegram Admin ID** (опционально)
   - Напишите [@userinfobot](https://t.me/userinfobot)
   - Получите ваш user ID

## Автоматическая установка

```bash
# 1. Клонирование репозитория
git clone https://github.com/yourusername/lilagentsbet.git
cd lilagentsbet

# 2. Запуск автоматической установки
chmod +x scripts/setup.sh
./scripts/setup.sh
```

## Ручная установка

### Шаг 1: Окружение
```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация (Linux/Mac)
source venv/bin/activate

# Активация (Windows)
venv\Scripts\activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt
```

### Шаг 2: Конфигурация
```bash
# Копирование примера конфигурации
cp .env.example .env

# Редактирование конфигурации
nano .env  # или любой другой редактор
```

Заполните следующие обязательные поля:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
ANTHROPIC_API_KEY=sk-ant-api03-your_key_here
TELEGRAM_ADMIN_ID=your_telegram_id
```

### Шаг 3: Запуск сервисов
```bash
# Запуск Docker контейнеров
docker-compose up -d

# Проверка статуса
docker-compose ps
```

Должны быть запущены:
- ✅ postgres (порт 5432)
- ✅ redis (порт 6379)  
- ✅ chromadb (порт 8000)
- ✅ n8n (порт 5678)

### Шаг 4: Инициализация базы знаний
```bash
# Загрузка документов в ChromaDB
python scripts/load_knowledge.py
```

### Шаг 5: Запуск бота
```bash
# Продакшн запуск
python src/main.py

# Разработка с автоперезагрузкой
./scripts/run_dev.sh
```

## Проверка установки

### 1. Проверка сервисов
```bash
# Проверка Redis
redis-cli ping
# Ответ: PONG

# Проверка PostgreSQL
docker exec -it lilagentsbet_postgres_1 psql -U postgres -d lil_agents -c "SELECT version();"

# Проверка ChromaDB
curl http://localhost:8000/api/v1/heartbeat
# Ответ: {"nanosecond heartbeat": ...}
```

### 2. Проверка бота
- Отправьте `/start` вашему боту
- Попробуйте команду `/help`
- Протестируйте `/status`

## Возможные проблемы

### Python зависимости
```bash
# Если ошибки с cryptography
pip install --upgrade cryptography

# Если проблемы с asyncio
pip install --upgrade asyncio

# Если проблемы с ChromaDB
pip install --upgrade chromadb sentence-transformers
```

### Docker проблемы
```bash
# Если порты заняты
docker-compose down
sudo lsof -i :5432 :6379 :8000 :5678
# Остановите конфликтующие сервисы

# Если проблемы с разрешениями
sudo usermod -aG docker $USER
# Перелогиньтесь
```

### Telegram бот не отвечает
1. Проверьте правильность токена
2. Убедитесь что бот не заблокирован
3. Проверите логи: `tail -f logs/bot_$(date +%Y%m%d).log`

### Anthropic API ошибки
1. Проверьте корректность ключа
2. Убедитесь что есть кредиты
3. Проверьте rate limits

## Мониторинг

### Логи
```bash
# Основные логи
tail -f logs/main_$(date +%Y%m%d).log

# Логи бота
tail -f logs/bot_$(date +%Y%m%d).log

# Логи агента
tail -f logs/lil_ken_ceo_$(date +%Y%m%d).log
```

### Веб интерфейсы
- **n8n**: http://localhost:5678 (admin/admin)
- **ChromaDB**: http://localhost:8000/docs

## Обновление

```bash
# Остановка бота
# Ctrl+C в терминале

# Обновление кода
git pull origin main

# Обновление зависимостей
pip install -r requirements.txt --upgrade

# Перезапуск сервисов
docker-compose restart

# Запуск бота
python src/main.py
```

## Развертывание в продакшн

### Системные настройки
```bash
# Увеличение лимитов
echo "* soft nofile 65536" >> /etc/security/limits.conf
echo "* hard nofile 65536" >> /etc/security/limits.conf

# Настройка swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Systemd сервис
```bash
# Создание сервиса
sudo cp scripts/lil_ken_ceo.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lil_ken_ceo
sudo systemctl start lil_ken_ceo
```

### Nginx прокси (опционально)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /n8n {
        proxy_pass http://localhost:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /chroma {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Поддержка

### Телеграм бот не запускается
1. Проверьте `.env` файл
2. Убедитесь что все сервисы запущены
3. Проверьте логи на ошибки

### Медленная работа
1. Увеличьте ресурсы Docker
2. Оптимизируйте PostgreSQL настройки
3. Проверьте загрузку сети

### Ошибки памяти
1. Увеличьте RAM для Docker
2. Настройте swap файл
3. Мониторьте потребление памяти

---

Если проблемы не решаются, создайте issue в GitHub или напишите в Telegram поддержку.