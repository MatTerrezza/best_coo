import telebot.types as types
import os


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_me = types.KeyboardButton("About me")
    btn_usl = types.KeyboardButton("Услуги")
    btn_aut = types.KeyboardButton("Автоматизация бизнес")
    btn_serv = types.KeyboardButton("FAQ")
    
    keyboard.add(btn_aut, btn_usl)    
    keyboard.add(btn_me, btn_serv)
    return keyboard

def get_pdf_button():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📄 Скачать чек-лист", callback_data="get_pdf"))
    return markup

def get_services_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_office = types.KeyboardButton("🖥Цифровой офис под ключ")
    btn_crm = types.KeyboardButton("🗂CRM")
    btn_tgbot = types.KeyboardButton("🤖Telegram бот")    
    btn_mapp = types.KeyboardButton("🌐Telegram Mini app")
    btn_integr = types.KeyboardButton("🔃Интеграции")
    btn_back = types.KeyboardButton("◀️Назад")
    
    keyboard.add(btn_office, btn_crm, btn_tgbot, btn_mapp, btn_integr, btn_back)
    return keyboard
    
def get_automatic_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_cons = types.KeyboardButton("Консультации")
    btn_audit = types.KeyboardButton("Глубинный аудит")
    btn_stsess = types.KeyboardButton("Стратегические сессии")
    btn_wow = types.KeyboardButton("WOW сервис")
    btn_back = types.KeyboardButton("◀️Назад")
    
    keyboard.add(btn_cons, btn_audit)
    keyboard.add(btn_stsess, btn_wow)
    keyboard.add(btn_back)
    return keyboard
