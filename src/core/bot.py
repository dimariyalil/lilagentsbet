"""
Простой Telegram бот
"""
import logging
from telegram import Update, BotCommand, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from agents.lil_ken_ceo.agent import LilKenCEO
from utils.config import settings

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class CEOBot:
    """Класс Telegram бота с ИИ агентом"""
    
    def __init__(self):
        """Инициализация бота"""
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self.ceo_agent = LilKenCEO()
        
        # Настраиваем обработчики
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка обработчиков команд"""
        # Команды
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("menu", self.cmd_menu))
        self.app.add_handler(CommandHandler("yearstrategy", self.cmd_year_strategy))
        self.app.add_handler(CommandHandler("marketanalysis", self.cmd_market_analysis))
        self.app.add_handler(CommandHandler("competitorwatch", self.cmd_competitor_watch))
        self.app.add_handler(CommandHandler("swotanalysis", self.cmd_swot_analysis))
        self.app.add_handler(CommandHandler("riskassessment", self.cmd_risk_assessment))
        self.app.add_handler(CommandHandler("dailyreport", self.cmd_daily_report))
        self.app.add_handler(CommandHandler("weeklyreport", self.cmd_weekly_report))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        
        # Обработчик callback кнопок
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Обработка текстовых сообщений (должна быть последней!)
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        user = update.effective_user
        welcome_text = f"""
🎯 Привет, {user.first_name}! Я lil_ken_ceo - твой виртуальный CEO.

Я помогу с:
• 📊 Стратегическим планированием  
• 📈 Анализом рынков и конкурентов
• ⚠️ Оценкой рисков и возможностей
• 💡 Принятием ключевых решений

Используй /help или /menu для списка команд.
"""
        
        # Создаем клавиатуру с основными командами
        keyboard = [
            [
                InlineKeyboardButton("📊 Меню команд", callback_data="menu"),
                InlineKeyboardButton("❓ Помощь", callback_data="help")
            ],
            [
                InlineKeyboardButton("📈 Анализ рынка", callback_data="market"),
                InlineKeyboardButton("🎯 Стратегия", callback_data="strategy")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"User {user.id} ({user.username}) started the bot")
    
    async def cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /menu - показать главное меню"""
        keyboard = [
            [
                InlineKeyboardButton("📊 Годовая стратегия", callback_data="yearstrategy"),
                InlineKeyboardButton("📈 Анализ рынка", callback_data="marketanalysis")
            ],
            [
                InlineKeyboardButton("👥 Конкуренты", callback_data="competitorwatch"),
                InlineKeyboardButton("⚖️ SWOT анализ", callback_data="swotanalysis")
            ],
            [
                InlineKeyboardButton("⚠️ Оценка рисков", callback_data="riskassessment"),
                InlineKeyboardButton("📋 Ежедневный отчет", callback_data="dailyreport")
            ],
            [
                InlineKeyboardButton("📅 Недельный отчет", callback_data="weeklyreport"),
                InlineKeyboardButton("⚙️ Статус", callback_data="status")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = """
🎯 **Главное меню lil_ken_ceo**

Выберите нужную функцию:

📊 **Аналитика:**
• Годовая стратегия
• Анализ рынка
• Оценка конкурентов

⚖️ **Планирование:**
• SWOT анализ
• Оценка рисков
• Отчеты

Или просто напишите мне вопрос! 💬
"""
        
        # Проверяем, это callback или обычная команда
        if update.callback_query:
            await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(menu_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "menu":
            # Для меню создаем фейковый update с message
            fake_update = Update(
                update_id=update.update_id,
                message=query.message,
                callback_query=query
            )
            await self.cmd_menu(fake_update, context)
        elif callback_data == "help":
            await self.cmd_help(update, context)
        elif callback_data == "market" or callback_data == "marketanalysis":
            await self.cmd_market_analysis(update, context)
        elif callback_data == "strategy" or callback_data == "yearstrategy":
            await self.cmd_year_strategy(update, context)
        elif callback_data == "competitorwatch":
            await self.cmd_competitor_watch(update, context)
        elif callback_data == "swotanalysis":
            await self.cmd_swot_analysis(update, context)
        elif callback_data == "riskassessment":
            await self.cmd_risk_assessment(update, context)
        elif callback_data == "dailyreport":
            await self.cmd_daily_report(update, context)
        elif callback_data == "weeklyreport":
            await self.cmd_weekly_report(update, context)
        elif callback_data == "status":
            await self.cmd_status(update, context)
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help"""
        help_text = """
📋 **Доступные команды:**

🎯 **Стратегия:**
/yearstrategy - Годовая стратегия развития
/swotanalysis - SWOT анализ компании  
/riskassessment - Оценка бизнес-рисков

📊 **Аналитика:**
/marketanalysis - Анализ нового рынка
/competitorwatch - Мониторинг конкурентов

📈 **Отчеты:**
/dailyreport - Ежедневный отчет
/weeklyreport - Недельный отчет

⚙️ **Другое:**
/menu - Главное меню с кнопками
/status - Статус системы
/help - Эта справка

💬 **Или просто напишите вопрос!**
Я отвечу как опытный CEO.
"""
        
        # Проверяем, это callback или обычная команда
        if update.callback_query:
            await update.callback_query.edit_message_text(help_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def _send_message(self, update: Update, text: str, parse_mode: str = None):
        """Универсальная функция для отправки сообщений (работает с callback и обычными сообщениями)"""
        if update.callback_query:
            await update.callback_query.message.reply_text(text, parse_mode=parse_mode)
        else:
            await update.message.reply_text(text, parse_mode=parse_mode)
    
    async def cmd_year_strategy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /yearstrategy"""
        await self._send_message(update, "🔄 Разрабатываю годовую стратегию...")
        
        response = await self.ceo_agent.generate_year_strategy()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_market_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /marketanalysis"""
        # Для callback запросов используем дефолтную страну
        if update.callback_query:
            country = "Россия"
        else:
            if not context.args:
                await self._send_message(update, "Укажите страну для анализа:\n/marketanalysis Бразилия")
                return
            country = " ".join(context.args)
        
        await self._send_message(update, f"🔍 Анализирую рынок {country}...")
        
        response = await self.ceo_agent.analyze_market(country)
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_competitor_watch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /competitorwatch"""
        await self._send_message(update, "👀 Собираю данные о конкурентах...")
        
        response = await self.ceo_agent.competitor_analysis()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_swot_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /swotanalysis"""
        await self._send_message(update, "📊 Провожу SWOT анализ...")
        
        response = await self.ceo_agent.swot_analysis()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_risk_assessment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /riskassessment"""
        await self._send_message(update, "⚠️ Оцениваю бизнес-риски...")
        
        response = await self.ceo_agent.risk_assessment()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_daily_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /dailyreport"""
        await self._send_message(update, "📋 Формирую ежедневный отчет...")
        
        response = await self.ceo_agent.daily_report()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_weekly_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /weeklyreport"""
        await self._send_message(update, "📅 Формирую недельный отчет...")
        
        response = await self.ceo_agent.weekly_report()
        await self._send_message(update, response, parse_mode='Markdown')
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /status"""
        status_text = f"""
⚙️ **Статус системы lil_ken_ceo**

🤖 **Бот:** Активен
🎯 **Агент:** {settings.AGENT_NAME}
🌍 **Язык:** {settings.AGENT_LANGUAGE}
📝 **Логи:** {settings.LOG_LEVEL}

🔑 **Конфигурация:**
• Telegram Bot: ✅ Подключен
• Anthropic API: ✅ Активен
• База знаний: ✅ Работает

💡 **Готов к работе!**
"""
        await self._send_message(update, status_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_message = update.message.text
        user_id = update.effective_user.id
        
        logger.info(f"Message from {user_id}: {user_message}")
        
        # Показываем "печатает..."
        await update.message.chat.send_action("typing")
        
        # Обрабатываем через агента
        response = await self.ceo_agent.process_message(user_message, user_id)
        
        # Отправляем ответ
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def setup_bot_commands(self):
        """Настройка команд в меню бота"""
        commands = [
            BotCommand("start", "Начать работу"),
            BotCommand("help", "Помощь"),
            BotCommand("yearstrategy", "Годовая стратегия"),
            BotCommand("marketanalysis", "Анализ рынка"),
            BotCommand("competitorwatch", "Мониторинг конкурентов"),
            BotCommand("swotanalysis", "SWOT анализ"),
            BotCommand("riskassessment", "Оценка рисков"),
            BotCommand("dailyreport", "Дневной отчет"),
            BotCommand("weeklyreport", "Недельный отчет"),
            BotCommand("status", "Статус системы"),
        ]
        await self.app.bot.set_my_commands(commands)
    
    async def start(self):
        """Запуск бота"""
        # Настраиваем команды
        await self.setup_bot_commands()
        
        # Инициализируем агента
        await self.ceo_agent.initialize()
        
        # Логируем информацию о запуске с username из конфигурации
        logger.info(f"🤖 Bot @{settings.TELEGRAM_BOT_USERNAME} started successfully!")
        logger.info(f"📊 Agent: {settings.AGENT_NAME}")
        logger.info(f"🌍 Language: {settings.AGENT_LANGUAGE}")
        logger.info(f"📝 Log level: {settings.LOG_LEVEL}")
        
        # Запускаем polling
        await self.app.run_polling(allowed_updates=Update.ALL_TYPES)