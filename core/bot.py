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
            from handlers.channel_handlers import ChannelHandlers
            from services.admin_commands import AdminCommands
            
            # Intentar importar TokenConfig si existe
            try:
                from states.admin_states import TokenConfig
            except ImportError:
                logger.warning("⚠️ TokenConfig no encontrado, continuando sin él")

            # Comandos básicos
            self.application.add_handler(CommandHandler("start", BaseHandlers.start))
            self.application.add_handler(CommandHandler("help", BaseHandlers.help_command))
            self.application.add_handler(CommandHandler("admin", AdminHandlers.admin_command))

            # ✅ COMANDOS DE ADMINISTRADOR
            self.application.add_handler(CommandHandler("register_channel", AdminCommands.register_channel_command))
            self.application.add_handler(CommandHandler("clear_channels", AdminCommands.clear_channels_command))
            self.application.add_handler(CommandHandler("list_channels", AdminCommands.list_channels_command))

            # ✅ UN SOLO HANDLER PARA TODOS LOS CALLBACKS
            self.application.add_handler(CallbackQueryHandler(BaseHandlers.button_handler))

            # ✅ AÑADIR HANDLER ESPECÍFICO PARA CANALES
            self.application.add_handler(
                CallbackQueryHandler(
                    ChannelHandlers.channel_management_handler,
                    pattern="^(channel_|admin_channels|register_|tariff_|set_price_|generate_token_|show_tariffs_|members_|config_|example_channels).*$"
                )
            )

            # Handlers para tokens (solo si existen los métodos)
            if hasattr(AdminHandlers, '_start_token_config'):
                self.application.add_handler(
                    CallbackQueryHandler(
                        AdminHandlers._start_token_config,
                        pattern="^admin_generate_token$"
                    )
                )
                
            if hasattr(AdminHandlers, 'handle_token_name_input'):
                self.application.add_handler(
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        AdminHandlers.handle_token_name_input
                    )
                )
                
            if hasattr(AdminHandlers, 'handle_token_duration_callback'):
                self.application.add_handler(
                    CallbackQueryHandler(
                        AdminHandlers.handle_token_duration_callback,
                        pattern="^token_duration_"
                    )
                )
                
            if hasattr(AdminHandlers, 'handle_token_price_input'):
                self.application.add_handler(
                    MessageHandler(
                        filters.TEXT & ~filters.COMMAND,
                        AdminHandlers.handle_token_price_input
                    )
                )

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
            
