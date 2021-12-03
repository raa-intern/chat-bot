import telebot
import os

from telebot import types
TOKEN = '2114765545:AAEl5fXQt6-BMyXKtxdwTPz8L_o7RjPe9Rk' #token here

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Вопросы/Ответы📌')
    item2 = types.KeyboardButton('Связь с менеджером👥')
    item3 = types.KeyboardButton('Отправить резюме')
    markup.add(item1, item2, item3)
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
            bot.send_message(message.chat.id, 'Менеджер (Имя): @manager')
        elif message.text == 'Отправить резюме':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Отправить файл')
            item2 = types.KeyboardButton('Заполнить google-form')
            back = types.KeyboardButton('Назад↩️')
            markup.add(item1, item2, back)
            bot.send_message(message.chat.id, 'Вы можете загрузить файл или заполнить google-form', reply_markup = markup)
        elif message.text == 'Назад↩️':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('Вопросы/Ответы📌')
            item2 = types.KeyboardButton('Связь с менеджером👥')
            item3 = types.KeyboardButton('Отправить резюме')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Вы можете найти здесь ответы на ваши вопросы касаемо стажировки, связаться с менеджером или отправить резюме', reply_markup = markup)
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
        elif message.text == 'Отправить файл':
            msg = bot.send_message(message.chat.id,"Выберите и отправьте файл. Доступные форматы для загрузки pdf, docx, txt.")
            bot.register_next_step_handler(msg, save_doc)
        elif message.text == 'Заполнить google-form':
            bot.send_message(message.chat.id, 'Перейдите по ссылке и заполните форму: https://docs.google.com/forms/u/0/')

#@bot.message_handler(content_types=['document'])
def save_doc(message): #function to store files locally
    if message.chat.type == 'private':
            try:
                file_inf = bot.get_file(message.document.file_id)
                file_upload = bot.download_file(file_inf.file_path)
                path = '/home/alxppv/bot/files/' + message.document.file_name
                extension = os.path.splitext(message.document.file_name)[1]
                #bot.reply_to(message, extension)
                if extension == ".txt" or extension == ".pdf" or extension == ".docx":
                    with open(path, 'wb') as new_file:
                        new_file.write(file_upload)
                    bot.reply_to(message, "Файл успешно добавлен!")
                else:
                    bot.reply_to(message, "Данный формат недоступен! Загрузите файл в формате pdf, txt или docx")
            except Exception as e:
                #bot.reply_to(message, e)
                bot.reply_to(message, 'Вы не выбрали файл!')
bot.polling(none_stop = True)

#need to do:
#sending a file to email
