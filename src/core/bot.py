"""
Основной Telegram бот для lil_ken_ceo
"""
import asyncio
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from agents.lil_ken_ceo.agent import LilKenCEO
from utils.config import settings
from utils.logger import setup_logger

logger = setup_logger("bot")


class CEOBot:
    """Главный класс бота"""
    
    def __init__(self):
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self.ceo_agent = LilKenCEO()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка обработчиков команд"""
        # Команды
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        self.app.add_handler(CommandHandler("yearstrategy", self.cmd_year_strategy))
        self.app.add_handler(CommandHandler("marketanalysis", self.cmd_market_analysis))
        self.app.add_handler(CommandHandler("competitorwatch", self.cmd_competitor_watch))
        self.app.add_handler(CommandHandler("swotanalysis", self.cmd_swot_analysis))
        self.app.add_handler(CommandHandler("riskassessment", self.cmd_risk_assessment))
        self.app.add_handler(CommandHandler("dailyreport", self.cmd_daily_report))
        self.app.add_handler(CommandHandler("weeklyreport", self.cmd_weekly_report))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        
        # Обработка текстовых сообщений
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        welcome_text = """
🎯 Привет! Я lil_ken_ceo - твой виртуальный CEO.

Я помогу с:
• Стратегическим планированием
• Анализом рынков и конкурентов
• Оценкой рисков и возможностей
• Принятием ключевых решений

Используй /help для списка команд.
"""
        await update.message.reply_text(welcome_text)
        logger.info(f"User {update.effective_user.id} started bot")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /help"""
        help_text = """
📋 Доступные команды:

🎯 Стратегия:
/yearstrategy - Годовая стратегия развития
/swotanalysis - SWOT анализ компании
/riskassessment - Оценка бизнес-рисков

📊 Аналитика:
/marketanalysis [страна] - Анализ нового рынка
/competitorwatch - Мониторинг конкурентов

📈 Отчеты:
/dailyreport - Ежедневный отчет
/weeklyreport - Еженедельный отчет

🔧 Система:
/status - Статус системы
/help - Эта справка

Просто напиши мне вопрос, и я помогу!
"""
        await update.message.reply_text(help_text)
    
    async def cmd_year_strategy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /yearstrategy"""
        await update.message.reply_text("🔄 Разрабатываю годовую стратегию...")
        
        response = await self.ceo_agent.generate_year_strategy()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_market_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /marketanalysis"""
        if not context.args:
            await update.message.reply_text(
                "Укажите страну для анализа:\n/marketanalysis Бразилия"
            )
            return
        
        country = " ".join(context.args)
        await update.message.reply_text(f"🔍 Анализирую рынок {country}...")
        
        response = await self.ceo_agent.analyze_market(country)
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_competitor_watch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /competitorwatch"""
        await update.message.reply_text("👀 Собираю данные о конкурентах...")
        
        response = await self.ceo_agent.competitor_analysis()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_swot_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /swotanalysis"""
        await update.message.reply_text("📊 Провожу SWOT анализ...")
        
        response = await self.ceo_agent.swot_analysis()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_risk_assessment(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /riskassessment"""
        await update.message.reply_text("⚠️ Оцениваю риски...")
        
        response = await self.ceo_agent.assess_risks()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_daily_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /dailyreport"""
        await update.message.reply_text("📊 Готовлю ежедневный отчет...")
        
        response = await self.ceo_agent.generate_daily_report()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_weekly_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /weeklyreport"""
        await update.message.reply_text("📈 Готовлю еженедельный отчет...")
        
        response = await self.ceo_agent.generate_weekly_report()
        await update.message.reply_text(response, parse_mode='Markdown')
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /status"""
        status = await self.ceo_agent.get_status()
        await update.message.reply_text(status, parse_mode='Markdown')
    
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