from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from .config import Config
from .database import init_db
import logging

logger = logging.getLogger(__name__)


class DianaBot:
    def __init__(self):
        logger.info("🔧 Inicializando DianaBot...")

        # Validar configuración
        try:
            Config.validate()
            logger.info("✅ Configuración validada")
        except Exception as e:
            logger.error(f"❌ Error en configuración: {e}")
            raise

        # Crear aplicación
        try:
            self.application = Application.builder().token(Config.BOT_TOKEN).build()
            logger.info("✅ Aplicación de Telegram creada")
        except Exception as e:
            logger.error(f"❌ Error creando aplicación: {e}")
            raise

    def setup_handlers(self):
        """Configura handlers básicos - VERSIÓN SIMPLIFICADA"""
        logger.info("🔧 Configurando handlers...")

        try:
            # Import handlers
            from handlers.base_handlers import BaseHandlers
            from handlers.admin_handlers import AdminHandlers

            # Comandos básicos
            self.application.add_handler(CommandHandler("start", BaseHandlers.start))
            self.application.add_handler(CommandHandler("help", BaseHandlers.help_command))
            self.application.add_handler(CommandHandler("admin", AdminHandlers.admin_command))

            # ✅ UN SOLO HANDLER PARA TODOS LOS CALLBACKS
            self.application.add_handler(CallbackQueryHandler(BaseHandlers.button_handler))

            logger.info("✅ Handlers configurados correctamente")

        except Exception as e:
            logger.error(f"❌ Error configurando handlers: {e}")
            raise

    def run(self):
        """Inicia el bot"""
        try:
            logger.info("🔧 Preparando bot para ejecución...")

            # Inicializar base de datos
            logger.info("📊 Inicializando base de datos...")
            init_db()
            logger.info("✅ Base de datos lista")

            # Configurar handlers
            logger.info("🎮 Configurando handlers...")
            self.setup_handlers()
            logger.info("✅ Handlers listos")

            # Iniciar polling
            logger.info("🎩 Lucien está listo para recibir invitados...")
            logger.info("🚀 Iniciando polling...")

            self.application.run_polling(
                allowed_updates=["message", "callback_query"], drop_pending_updates=True
            )

        except Exception as e:
            logger.error(f"❌ Error ejecutando bot: {e}")
            raise
