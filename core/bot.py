from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from .config import Config
from .database import init_db
import logging

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DianaBot:
    def __init__(self):
        # Validar configuración antes de inicializar
        Config.validate()
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
    
    def setup_handlers(self):
        """Configura todos los handlers del bot"""
        logger.info("Configurando handlers...")
        
        # Importar handlers
        from handlers.base_handlers import BaseHandlers
        from handlers.mission_handlers import MissionHandlers
        from handlers.game_handlers import GameHandlers
        from handlers.story_handlers import StoryHandlers
        
        # Comandos básicos
        self.application.add_handler(CommandHandler("start", BaseHandlers.start))
        self.application.add_handler(CommandHandler("help", BaseHandlers.help_command))
        
        # Callback queries principales
        self.application.add_handler(CallbackQueryHandler(
            BaseHandlers.button_handler, 
            pattern="^(main_menu|profile|missions|games|story)$"
        ))
        
        # Callback queries de misiones
        self.application.add_handler(CallbackQueryHandler(
            MissionHandlers.mission_handler,
            pattern="^mission_"
        ))
        
        # Callback queries de juegos
        self.application.add_handler(CallbackQueryHandler(
            GameHandlers.game_handler,
            pattern="^game_"
        ))
        
        # Callback queries de historia
        self.application.add_handler(CallbackQueryHandler(
            StoryHandlers.story_handler,
            pattern="^story_"
        ))
        
        logger.info("✅ Handlers configurados correctamente")
    
    def run(self):
        """Inicia el bot"""
        try:
            logger.info("🚀 Iniciando DianaBot...")
            
            # Inicializar base de datos
            init_db()
            
            # Configurar handlers
            self.setup_handlers()
            
            # Iniciar scheduler
            from jobs.scheduler import start_scheduler
            start_scheduler()
            
            # Iniciar polling
            logger.info("🎩 Lucien está listo para recibir invitados...")
            self.application.run_polling(allowed_updates=['message', 'callback_query'])
            
        except Exception as e:
            logger.error(f"❌ Error al iniciar el bot: {e}")
            raise
