#! /usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
import os
import smtplib
import configparser

from telebot import types
from email.message import EmailMessage
from email.headerregistry import Address
from email.mime.application import MIMEApplication

config = configparser.ConfigParser()
config.read("settings.ini")

bot = telebot.TeleBot(config["Main"]["Token"])

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
            bot.register_next_step_handler(msg, save_and_send_cv)
        elif message.text == 'Заполнить google-form':
            bot.send_message(message.chat.id, 'Перейдите по ссылке и заполните форму: https://docs.google.com/forms/u/0/')

#@bot.message_handler(content_types=['document'])
def save_and_send_cv(message):
    if message.chat.type == 'private':
        try:
            file_inf = bot.get_file(message.document.file_id)
            file_upload = bot.download_file(file_inf.file_path)
        except Exception as e:
            bot.reply_to(message, e)

        if(os.path.isdir('./files') != True):
            os.mkdir('./files', 755)

        path = './files/' + message.document.file_name
        extension = os.path.splitext(message.document.file_name)[1]
        allow_ext = [".txt", ".pdf", ".docx"]

        if extension in allow_ext:
            with open(path, 'wb') as cv:
                cv.write(file_upload)

            with open(path, 'rb') as cv:
                msg = EmailMessage()
                msg['From'] = Address(display_name='Recipient', addr_spec=config["Smtp"]["User"])
                msg['To'] = Address(display_name='Sender', addr_spec=config["Smtp"]["To"])
                msg['Subject'] = 'Alert! new CV'
                msg.set_content('New CV from telegram bot.')

                att = MIMEApplication(cv.read(),_subtype=extension)
                att.add_header('Content-Disposition', 'attachment', filename=message.document.file_name)
                msg.make_mixed()
                msg.attach(att)

                try:
                    server = smtplib.SMTP_SSL(config["Smtp"]["Host"], config["Smtp"]["Port"])
                    server.ehlo()
                    server.login(config["Smtp"]["User"], config["Smtp"]["Password"])
                    server.sendmail(config["Smtp"]["User"], config["Smtp"]["To"], msg.as_string())
                    server.close()

                    bot.reply_to(message, "Файл успешно отправлен!")
                except Exception as e:
                    bot.send_message(message.chat.id, e)

        else:
            bot.reply_to(message, "Данный формат недоступен! Загрузите файл в формате pdf, txt или docx")

bot.polling(none_stop = True)