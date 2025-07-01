import telebot
import buttons
import database
import json
import time
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv
from buttons import get_main_keyboard, get_services_keyboard, get_automatic_keyboard

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
ADMIN_ID = os.getenv("ADMIN_ID")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id  # Получаем ID пользователя
    database.add_user_if_not_exists(user_id, message.from_user.username)
    
    welcome_text = (
        f"<b>Telegram-боты и Mini Apps – твой бизнес на автопилоте</b>\n\n"
        f"Привет, {user_name}!\n\n"
    )

    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=buttons.get_main_keyboard(),
        parse_mode='HTML'
    )
    
    # Добавляем отправку сообщения с inline-кнопкой
    bot.send_message(
        message.chat.id,
        "Хотите получить чек-лист?",
        reply_markup=buttons.get_pdf_button()
    )

@bot.callback_query_handler(func=lambda call: call.data == "get_pdf")
def send_pdf(call):
    with open("checklist.pdf", "rb") as file:
        bot.send_document(
            call.message.chat.id,
            file,
            caption="Ваш чек-лист"
        )
    bot.answer_callback_query(call.id)
    

@bot.message_handler(func=lambda m: m.text == "About me")
def send_me(message):
    bot.send_message(message.chat.id, ".......................")

@bot.message_handler(func=lambda message: message.text == "Автоматизация бизнес")
def show_automation(message):
    bot.send_message(
        message.chat.id,
        "Выберите вариант автоматизации:",
        reply_markup=buttons.get_automatic_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "Консультации")
def send_cons(message):
    bot.send_message(message.chat.id, ".......................")
    
@bot.message_handler(func=lambda m: m.text == "Глубинный аудит")
def send_aut(message):
    bot.send_message(message.chat.id, ".......................")
    
@bot.message_handler(func=lambda m: m.text == "Стратегические сессии")
def send_stsess(message):
    bot.send_message(message.chat.id, ".......................")

@bot.message_handler(func=lambda m: m.text == "WOW сервис")
def send_wow(message):
    bot.send_message(message.chat.id, ".......................")

@bot.message_handler(func=lambda message: message.text == "Услуги") #Раскрывающаяся reply клава
def show_services(message):
   
    bot.send_message(
        message.chat.id,
        "Выберите нужную услугу:",
        reply_markup=buttons.get_services_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == "◀️Назад")  # обработчик кнопки назад
def back_to_main(message):
    bot.send_message(
        message.chat.id,
        "Главное меню:",
        reply_markup=buttons.get_main_keyboard()
    )

# --- Команды управления пользователями
@bot.message_handler(commands=['adduser'])
def add_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ У вас нет прав на эту команду.")
        return

    try:
        _, user_id_str, username = message.text.split()
        user_id = int(user_id_str)
        database.add_user(user_id, username)
        bot.reply_to(message, f"✅ Пользователь {user_id} добавлен.")
    except Exception:
        bot.reply_to(message, "❌ Использование: /adduser <id> <username>")


@bot.message_handler(commands=['deluser'])
def del_user(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ У вас нет прав на эту команду.")
        return

    try:
        _, user_id_str = message.text.split()
        user_id = int(user_id_str)
        database.remove_user(user_id)
        bot.reply_to(message, f"✅ Пользователь {user_id} удалён.")
    except Exception:
        bot.reply_to(message, "❌ Использование: /deluser <id>")

@bot.message_handler(commands=['stats']) # Статистика ну очевидно же что она делает 
def show_stats(message):
    if str(message.from_user.id) != ADMIN_ID:
        return
    
    top_commands = database.get_top_commands()
    response = "📊 Статистика команд:\n" + "\n".join(
        f"{cmd}: {count} раз" for cmd, count in top_commands
    )
    bot.reply_to(message, response)



#Запуск бота
def run_bot():
    print("🤖 Telegram-бот запущен...")
    database.init_db()
    
    while True:
        try:
            print("Запуск бота...")
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"⚠️ Произошла ошибка: {e}")
            traceback.print_exc()  # Печать полного стека ошибки для диагностики
            print("Перезапуск бота через 5 секунд...")
            time.sleep(5)  # Пауза перед перезапуском
