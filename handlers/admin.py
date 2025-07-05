from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_admin_menu
from utils.decorators import admin_only
from services.admin_service import AdminService


class AdminHandlers:
    @staticmethod
    @admin_only
    async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "\ud83d\udee0\ufe0f Bienvenido al glorioso panel de administraci\u00f3n. Trata de no romper nada.",
            reply_markup=get_admin_menu()
        )

    @staticmethod
    @admin_only
    async def admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        service = AdminService()
        if query.data == "admin_stats":
            stats = await service.get_basic_stats()
            text = (
                f"\ud83d\udc65 Usuarios registrados: {stats['users']}\n"
                f"\ud83d\udd11 Tokens VIP: {stats['vip_tokens']}"
            )
            await query.edit_message_text(text, reply_markup=get_admin_menu())
        elif query.data == "admin_generate_token":
            token = await service.generate_vip_token()
            await query.edit_message_text(
                f"\ud83d\udd11 Token generado: `{token}`",
                reply_markup=get_admin_menu(),
                parse_mode="Markdown"
            )
        elif query.data == "admin_broadcast":
            await query.edit_message_text(
                "Env\u00eda el mensaje a difundir usando /broadcast <texto>",
                reply_markup=get_admin_menu()
            )
        else:
            await query.edit_message_text(
                "Acci\u00f3n no reconocida.", reply_markup=get_admin_menu()
            )

    @staticmethod
    @admin_only
    async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        service = AdminService()
        stats = await service.get_basic_stats()
        await update.message.reply_text(
            f"\ud83d\udc65 Usuarios registrados: {stats['users']}\n"
            f"\ud83d\udd11 Tokens VIP: {stats['vip_tokens']}"
        )

    @staticmethod
    @admin_only
    async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not context.args:
            await update.message.reply_text("Uso: /broadcast <mensaje>")
            return
        message = " ".join(context.args)
        service = AdminService()
        await service.broadcast(context.bot, message)
        await update.message.reply_text("Mensaje enviado")
