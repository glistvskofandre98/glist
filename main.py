import telebot 
from telebot import types # Імпортуємо types для роботи з кнопками

TOKEN = "7815408165:AAEfu20IWpQdmyCRB9yu2kt9UnlGsV_OikU"

# Об'єкт бота
bot = telebot.TeleBot(TOKEN)

PRODUCTS = {
    "product_1": "Камінь (звичайний)",
    "product_2": "Палка (хрупка)",
    "product_3": "Повітря (з парижа)",
    "product_4": "Самоцвіт (проста)",
}

def create_main_menu_keyboard():
    

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
    one_time_keyboard=False)

    btn_view_products = types.KeyboardButton("🧺Переглянути ціності")
    btn_contact_us = types.KeyboardButton("☎️ Зв'язатись з нами")

    keyboard.add(btn_view_products)
    keyboard.add(btn_contact_us)
    return keyboard

def create_products_inline_keyboard():
    """Створює інлайн-клавіатуру для кожного товару. Ці кнопки прікріплюються до повідомлення"""

    keyboard = types.InlineKeyboardMarkup()
    
    # Проходимся по нашому словнику товарів
    for product_id, product_name in PRODUCTS.items():
        button = types.InlineKeyboardButton(f"Купити {product_name}💵",
        callback_data=f"buy_{product_id}")
        keyboard.add(button)
    btn_back_to_main = types.InlineKeyboardButton("🔙 Головне меню",
    callback_data="back_to_main")    
    keyboard.add(btn_back_to_main)

    return keyboard

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """Обробник команди /start і /help. Надсилає привітання і відкриває головне меню"""

    welcome_text = "Привіт! Ласкаво просимо до нашого магазину!"
    bot.send_message(message.chat.id, welcome_text, 
    reply_markup=create_main_menu_keyboard())

@bot.message_handler(func=lambda message:True)
def handler_text_messages(message):
    """Обробник текстових повідомлень від користуча.
    Розпізнає текст кнопок головного меню"""

    if message.text == "🧺Переглянути ціності":
        product_list = "Ось наші товари: \n\n"
        
        # Формуємо список товарів для виведення
        for product_id, product_name in PRODUCTS.items():
            product_list += f" - {product_name}\n"

        product_list += "\nОберіть товар, який бажаєте придбати:"

        # Надсилаємо список товарів з інлайн-кнопками
        bot.send_message(message.chat.id, product_list,
        reply_markup=create_products_inline_keyboard())

    elif message.text == "☎️ Зв'язатись з нами":
        contact_info = "Зв'яжіться з нами:\n\n" \
                        "А ні, не вийде:). Жартую:\n\n" \
                        "Номер:380 66 794 39 20:"
        bot.send_message(message.chat.id, contact_info,
        reply_markup=create_main_menu_keyboard())

    else:
        bot.send_message(message.chat.id, "Ваша команда для мене тупа..",
        reply_markup=create_main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Обробник натискань інлайн-кнопок"""

    bot.answer_callback_query(call.id)
    
    if call.data.startswith("buy_"):
        product_id = call.data.replace("buy_", "")
        product_name = PRODUCTS.get(product_id, "Невідомий товар")

        response_text = f"👌 Вітаємо, ви придбали собі {product_name}"
        
        bot.send_message(call.message.chat.id, response_text,
        reply_markup=create_main_menu_keyboard())

    elif call.data == "back_to_main":
        bot.send_message(call.message.chat.id, "Ви повернулися до головного меню",
        reply_markup=create_main_menu_keyboard())


print("Бот запущено! Шукай в Telegram! ЗРОЗУМІВ!?!?!?")
bot.infinity_polling()
