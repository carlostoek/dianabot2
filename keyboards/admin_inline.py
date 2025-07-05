from telegram import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton(text="\ud83d\udcca Estad\u00edsticas", callback_data="admin_stats")],
        [InlineKeyboardButton(text="\ud83c\udf7e Generar Token VIP", callback_data="admin_generate_token")],
        [InlineKeyboardButton(text="\ud83d\xdce3 Broadcast", callback_data="admin_broadcast")],
    ]
    return InlineKeyboardMarkup(keyboard)
