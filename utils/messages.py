
def welcome_message(user):
    return f"""
🍹 Oh, un usuario más... {user.first_name}, acompáñame, supongo.

Aquí comenzarás a recolectar piezas de una historia que probablemente no te hará más interesante.

¿Qué deseas hacer primero?
""".strip()

def backpack_message(backpack):
    if not backpack:
        return "👜 Tu colección miserable está vacía."

    message = "👜 Estas son tus piezas de lore:\n\n"
    for item in backpack:
        message += f"🔹 <b>{item['title']}</b>\n{item['description']}\n🌟 Rareza: {item['rarity']}\n\n"
    return message
