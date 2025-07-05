from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import get_db_session
from services.channel_service import ChannelService
from models.channel import ChannelType
from utils.keyboards import admin_keyboards
import logging

logger = logging.getLogger(__name__)

class ChannelHandlers:
    """Handlers para gestión de canales"""

    @staticmethod
    async def channel_management_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler principal para gestión de canales - EXPANDIDO"""
        try:
            query = update.callback_query
            await query.answer()

            if query.data == "admin_channels":
                await ChannelHandlers._show_channel_menu(query)
            elif query.data == "channel_register":
                await ChannelHandlers._show_register_options(query)
            elif query.data == "channel_list":
                await ChannelHandlers._show_channel_list(query)
            elif query.data == "channel_tariffs":
                await ChannelHandlers._show_tariff_management(query)
            elif query.data == "register_vip":
                await ChannelHandlers._start_vip_registration(query)
            elif query.data == "register_free":
                await ChannelHandlers._start_free_registration(query)
            elif query.data == "example_channels":
                await ChannelHandlers._show_example_channels(query)
            elif query.data.startswith("channel_"):
                channel_id = query.data.split("_")[1]
                await ChannelHandlers._show_channel_details(query, int(channel_id))
            elif query.data.startswith("create_tariff_"):
                channel_id = query.data.split("_")[2]
                await ChannelHandlers._show_tariff_creation(query, int(channel_id))
            elif query.data.startswith("tariff_duration_"):
                # Manejar selección de duración de tarifa
                parts = query.data.split("_")
                channel_id, days = int(parts[2]), int(parts[3])
                await ChannelHandlers._set_tariff_duration(query, channel_id, days)
            elif query.data.startswith("set_price_"):
                parts = query.data.split("_")
                channel_id, days, price = int(parts[2]), int(parts[3]), int(parts[4])
                await ChannelHandlers._create_tariff_final(query, channel_id, days, price)
            elif query.data.startswith("show_tariffs_"):
                channel_id = int(query.data.split("_")[2])
                await ChannelHandlers._show_channel_tariffs_for_tokens(query, channel_id)
            elif query.data.startswith("generate_token_"):
                tariff_id = int(query.data.split("_")[2])
                await ChannelHandlers._generate_token(query, tariff_id)

        except Exception as e:
            logger.error(f"Error en channel_management_handler: {e}")
            await query.edit_message_text("❌ Error procesando gestión de canales.")

    @staticmethod
    async def _show_channel_menu(query):
        """Muestra el menú principal de gestión de canales"""
        db = get_db_session()

        try:
            channels = ChannelService.get_channels(db)

            text = (
                "📢 Gestión de Canales\n\n"
                f"Canales registrados: {len(channels)}\n\n"
                "Selecciona una opción:"
            )

            keyboard = [
                [InlineKeyboardButton("➕ Registrar Canal", callback_data="channel_register")],
                [InlineKeyboardButton("📋 Ver Canales", callback_data="channel_list")],
                [InlineKeyboardButton("💰 Gestionar Tarifas", callback_data="channel_tariffs")],
                [InlineKeyboardButton("🎫 Generar Tokens", callback_data="channel_tokens")],
                [InlineKeyboardButton("◀️ Panel Admin", callback_data="admin_menu")]
            ]

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        finally:
            db.close()

    # Métodos placeholder para futuras implementaciones
    @staticmethod
    async def _show_register_options(query):
        """Muestra opciones para registrar canal"""
        text = (
            "➕ Registrar Nuevo Canal\n\n"
            "Selecciona el tipo de canal:"
        )

        keyboard = [
            [InlineKeyboardButton("💎 Canal VIP", callback_data="register_vip")],
            [InlineKeyboardButton("🆓 Canal Gratuito", callback_data="register_free")],
            [InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    async def _show_channel_list(query):
        """Muestra lista de canales registrados"""
        db = get_db_session()

        try:
            channels = ChannelService.get_channels(db)

            text = "📋 Canales Registrados\n\n"

            if not channels:
                text += "No hay canales registrados aún."
            else:
                for channel in channels:
                    emoji = "💎" if channel.channel_type.value == "vip" else "🆓"
                    status = "🟢" if channel.is_active else "🔴"
                    text += f"{emoji} {status} {channel.channel_name}\n"
                    text += f"   ID: {channel.channel_id}\n"
                    text += f"   Tipo: {channel.channel_type.value.upper()}\n\n"

            keyboard = [
                [InlineKeyboardButton("➕ Registrar Canal", callback_data="channel_register")],
                [InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")]
            ]

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        finally:
            db.close()

    @staticmethod
    async def _show_tariff_management(query):
        """Muestra gestión de tarifas - MEJORADO"""
        db = get_db_session()

        try:
            # Obtener canales VIP
            from models.channel import Channel, ChannelType
            vip_channels = db.query(Channel).filter(
                Channel.channel_type == ChannelType.VIP,
                Channel.is_active == True
            ).all()

            if not vip_channels:
                text = (
                    "💰 Gestión de Tarifas\n\n"
                    "❌ No hay canales VIP registrados.\n"
                    "Registra un canal VIP primero para crear tarifas."
                )
                keyboard = [
                    [InlineKeyboardButton("➕ Registrar Canal VIP", callback_data="register_vip")],
                    [InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")]
                ]
            else:
                text = "💰 Gestión de Tarifas\n\nSelecciona un canal VIP:"

                keyboard = []
                for channel in vip_channels:
                    tariffs_count = len(ChannelService.get_channel_tariffs(db, channel.id))
                    keyboard.append([InlineKeyboardButton(
                        f"💎 {channel.channel_name} ({tariffs_count} tarifas)",
                        callback_data=f"channel_{channel.id}"
                    )])

                keyboard.append([InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")])

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        finally:
            db.close()

    @staticmethod
    async def _start_vip_registration(query):
        """Inicia el proceso de registro de canal VIP"""
        text = (
            "💎 Registro de Canal VIP\n\n"
            "Para registrar un canal VIP necesitas:\n"
            "1. ID del canal (número)\n"
            "2. Nombre del canal\n\n"
            "📝 Ejemplo de ID: -1001234567890\n"
            "💡 Tip: Añade el bot al canal como administrador primero\n\n"
            "🚧 Función de registro interactivo en desarrollo.\n"
            "Por ahora, usa el comando manual."
        )

        keyboard = [
            [InlineKeyboardButton("📋 Canales de Ejemplo", callback_data="example_channels")],
            [InlineKeyboardButton("◀️ Volver", callback_data="channel_register")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    async def _start_free_registration(query):
        """Inicia el proceso de registro de canal gratuito"""
        text = (
            "🆓 Registro de Canal Gratuito\n\n"
            "Para registrar un canal gratuito necesitas:\n"
            "1. ID del canal (número)\n"
            "2. Nombre del canal\n"
            "3. Configurar delay de aceptación\n"
            "4. Mensaje de bienvenida\n\n"
            "🚧 Función de registro interactivo en desarrollo.\n"
            "Por ahora, usa el comando manual."
        )

        keyboard = [
            [InlineKeyboardButton("📋 Canales de Ejemplo", callback_data="example_channels")],
            [InlineKeyboardButton("◀️ Volver", callback_data="channel_register")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    async def _show_example_channels(query):
        """Muestra ejemplos de configuración de canales"""
        text = (
            "📋 **Ejemplos de Configuración**\n\n"
            "💎 **Canal VIP:**\n"
            "`/register_channel vip -1001234567890 Canal VIP Diana`\n\n"
            "🆓 **Canal Gratuito:**\n"
            "`/register_channel free -1001234567891 Canal Gratuito Diana`\n\n"
            "📝 **Cómo obtener el ID del canal:**\n"
            "1. Añade @userinfobot al canal\n"
            "2. El bot te dará el ID del canal\n"
            "3. Usa ese ID en el comando\n\n"
            "⚠️ **Importante:** El bot debe ser administrador del canal"
        )

        keyboard = [
            [InlineKeyboardButton("📋 Listar Canales", callback_data="channel_list")],
            [InlineKeyboardButton("◀️ Volver", callback_data="channel_register")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    @staticmethod
    async def _show_channel_details(query, channel_id):
        """Muestra detalles de un canal específico"""
        db = get_db_session()

        try:
            from models.channel import Channel
            channel = db.query(Channel).filter(Channel.id == channel_id).first()

            if not channel:
                await query.edit_message_text("❌ Canal no encontrado")
                return

            # Obtener tarifas del canal
            tariffs = ChannelService.get_channel_tariffs(db, channel_id)

            emoji = "💎" if channel.channel_type.value == "vip" else "🆓"
            text = (
                f"{emoji} {channel.channel_name}\n\n"
                f"📊 **Detalles del Canal:**\n"
                f"• ID: `{channel.channel_id}`\n"
                f"• Tipo: {channel.channel_type.value.upper()}\n"
                f"• Estado: {'🟢 Activo' if channel.is_active else '🔴 Inactivo'}\n"
                f"• Tarifas configuradas: {len(tariffs)}\n\n"
            )

            if tariffs:
                text += "💰 **Tarifas disponibles:**\n"
                for tariff in tariffs:
                    text += f"• {tariff.name}: {tariff.duration_days} días - {tariff.price_besitos} besitos\n"
            else:
                text += "⚠️ No hay tarifas configuradas"

            keyboard = []

            if channel.channel_type.value == "vip":
                keyboard.extend([
                    [InlineKeyboardButton("💰 Crear Tarifa", callback_data=f"create_tariff_{channel_id}")],
                    [InlineKeyboardButton("🎫 Generar Token", callback_data=f"show_tariffs_{channel_id}")],
                ])

            keyboard.extend([
                [InlineKeyboardButton("👥 Ver Miembros", callback_data=f"members_{channel_id}")],
                [InlineKeyboardButton("⚙️ Configurar", callback_data=f"config_{channel_id}")],
                [InlineKeyboardButton("◀️ Volver", callback_data="channel_list")]
            ])

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

        finally:
            db.close()

    @staticmethod
    async def _show_tariff_creation(query, channel_id):
        """Muestra opciones para crear tarifa"""
        text = (
            "💰 Crear Nueva Tarifa\n\n"
            "Selecciona la duración:"
        )

        keyboard = [
            [
                InlineKeyboardButton("1 Día", callback_data=f"tariff_duration_{channel_id}_1"),
                InlineKeyboardButton("1 Semana", callback_data=f"tariff_duration_{channel_id}_7")
            ],
            [
                InlineKeyboardButton("2 Semanas", callback_data=f"tariff_duration_{channel_id}_14"),
                InlineKeyboardButton("1 Mes", callback_data=f"tariff_duration_{channel_id}_30")
            ],
            [InlineKeyboardButton("◀️ Volver", callback_data=f"channel_{channel_id}")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    @staticmethod
    async def _set_tariff_duration(query, channel_id, days):
        """Configura la duración de la tarifa y pide el precio"""
        # Guardar en context para el siguiente paso (no implementado)
        context_data = {
            'channel_id': channel_id,
            'duration_days': days,
            'step': 'waiting_price'
        }

        duration_text = {
            1: "1 Día",
            7: "1 Semana",
            14: "2 Semanas",
            30: "1 Mes"
        }.get(days, f"{days} días")

        text = (
            f"💰 Nueva Tarifa - {duration_text}\n\n"
            f"Duración seleccionada: **{duration_text}**\n\n"
            f"💋 Precio sugerido:\n"
            f"• 1 Día: 100 besitos\n"
            f"• 1 Semana: 500 besitos\n"
            f"• 2 Semanas: 900 besitos\n"
            f"• 1 Mes: 1500 besitos\n\n"
            f"Selecciona el precio:"
        )

        # Precios sugeridos basados en duración
        suggested_prices = {
            1: [50, 100, 150],
            7: [300, 500, 700],
            14: [600, 900, 1200],
            30: [1000, 1500, 2000]
        }

        prices = suggested_prices.get(days, [100, 500, 1000])

        keyboard = [
            [InlineKeyboardButton(f"{price} besitos", callback_data=f"set_price_{channel_id}_{days}_{price}") for price in prices],
            [InlineKeyboardButton("◀️ Volver", callback_data=f"create_tariff_{channel_id}")]
        ]

        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    @staticmethod
    async def _show_channel_tariffs_for_tokens(query, channel_id):
        """Muestra tarifas de un canal para generar tokens"""
        db = get_db_session()

        try:
            tariffs = ChannelService.get_channel_tariffs(db, channel_id)

            if not tariffs:
                text = (
                    "🎫 Generar Tokens\n\n"
                    "❌ No hay tarifas configuradas para este canal.\n"
                    "Crea una tarifa primero."
                )
                keyboard = [
                    [InlineKeyboardButton("💰 Crear Tarifa", callback_data=f"create_tariff_{channel_id}")],
                    [InlineKeyboardButton("◀️ Volver", callback_data=f"channel_{channel_id}")]
                ]
            else:
                text = "🎫 Generar Token\n\nSelecciona una tarifa:"

                keyboard = []
                for tariff in tariffs:
                    keyboard.append([InlineKeyboardButton(
                        f"{tariff.name} - {tariff.price_besitos} besitos",
                        callback_data=f"generate_token_{tariff.id}"
                    )])

                keyboard.append([InlineKeyboardButton("◀️ Volver", callback_data=f"channel_{channel_id}")])

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

        finally:
            db.close()

    @staticmethod
    async def _generate_token(query, tariff_id):
        """Genera un token de acceso"""
        db = get_db_session()

        try:
            # Generar token
            link = ChannelService.generate_entry_token(db, tariff_id, query.from_user.id)

            text = (
                f"🎫 **Token Generado Exitosamente**\n\n"
                f"🔗 **Link de acceso:**\n"
                f"`{link}`\n\n"
                f"📋 **Instrucciones:**\n"
                f"1. Copia el link\n"
                f"2. Envíalo al usuario\n"
                f"3. El usuario hace clic y obtiene acceso\n\n"
                f"⏰ El token expira según la duración configurada"
            )

            keyboard = [
                [InlineKeyboardButton("🔄 Generar Otro", callback_data=f"generate_token_{tariff_id}")],
                [InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")]
            ]

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

        except Exception as e:
            await query.edit_message_text(
                f"❌ Error generando token: {str(e)}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("◀️ Volver", callback_data="admin_channels")
                ]])
            )
        finally:
            db.close()

    @staticmethod
    async def _create_tariff_final(query, channel_id, days, price):
        """Crea la tarifa final con todos los datos"""
        db = get_db_session()

        try:
            # Crear nombre automático
            duration_text = {
                1: "1 Día",
                7: "1 Semana",
                14: "2 Semanas",
                30: "1 Mes"
            }.get(days, f"{days} días")

            tariff_name = f"VIP {duration_text}"

            # Crear tarifa
            tariff = ChannelService.create_tariff(db, channel_id, tariff_name, days, price)

            text = (
                f"✅ **Tarifa Creada Exitosamente**\n\n"
                f"📋 **Detalles:**\n"
                f"• Nombre: {tariff.name}\n"
                f"• Duración: {tariff.duration_days} días\n"
                f"• Precio: {tariff.price_besitos} besitos\n\n"
                f"🎫 Ya puedes generar tokens con esta tarifa"
            )

            keyboard = [
                [InlineKeyboardButton("🎫 Generar Token", callback_data=f"generate_token_{tariff.id}")],
                [InlineKeyboardButton("💰 Crear Otra Tarifa", callback_data=f"create_tariff_{channel_id}")],
                [InlineKeyboardButton("◀️ Ver Canal", callback_data=f"channel_{channel_id}")]
            ]

            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )

        except Exception as e:
            await query.edit_message_text(
                f"❌ Error creando tarifa: {str(e)}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("◀️ Volver", callback_data=f"channel_{channel_id}")
                ]])
            )
        finally:
            db.close()
