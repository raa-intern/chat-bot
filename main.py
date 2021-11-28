import telebot
from telebot import types
TOKEN = '2114765545:AAEl5fXQt6-BMyXKtxdwTPz8L_o7RjPe9Rk'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Вопросы/Ответы📌')
    item2 = types.KeyboardButton('Связь с менеджером')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Приветствуем тебя, {0.first_name}! Это "Тестовая компания". Вы можете найти здесь ответы на ваши вопросы касаемо стажировки или связаться с менеджером'.format(message.from_user), reply_markup = markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Вопросы/Ответы📌':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Условия📝')
            item2 = types.KeyboardButton('Оплата💵')
            item3 = types.KeyboardButton('Место🏢')
            item4 = types.KeyboardButton('Время🕑')
            item5 = types.KeyboardButton('Требования📊')
            back = types.KeyboardButton('Назад↩️')
            markup.add(item1, item2, item3, item4, item5, back)
            bot.send_message(message.chat.id, 'Тут вы можете найти ответы на самые часто задаваемые вопросы ', reply_markup = markup)
        elif message.text == 'Связь с менеджером👥':
            bot.send_message(message.chat.id, 'Менеджер (Имя): @manager_for_example_name')
        elif message.text == 'Назад↩️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Вопросы/Ответы📌')
            item2 = types.KeyboardButton('Связь с менеджером👥')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Вы можете найти здесь ответы на ваши вопросы касаемо стажировки или связаться с менеджером', reply_markup = markup)
        elif message.text == 'Условия📝':
            bot.send_message(message.chat.id, 'Тут будут находиться условия работы')
        elif message.text == 'Оплата💵':
            bot.send_message(message.chat.id, 'Тут будут находиться оплата работы')
        elif message.text == 'Место🏢':
            bot.send_message(message.chat.id, 'Тут будут находиться место работы')
        elif message.text == 'Время🕑':
            bot.send_message(message.chat.id, 'Тут будут находиться время работы')
        elif message.text == 'Требования📊':
            bot.send_message(message.chat.id, 'Тут будут находиться требование работы')
bot.polling(none_stop = True)