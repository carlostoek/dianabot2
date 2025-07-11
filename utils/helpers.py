
def format_backpack(backpack):
    if not backpack:
        return "👜 Tu colección miserable está vacía."

    message = "👜 Estas son tus piezas de lore:\n\n"
    for item in backpack:
        message += f"🔹 <b>{item['title']}</b>\n{item['description']}\n🌟 Rareza: {item['rarity']}\n\n"
    return message
