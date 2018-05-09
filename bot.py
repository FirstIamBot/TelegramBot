#!/usr/bin/env python
# https://habrahabr.ru/post/346606/
# -*- coding: utf-8 -*-
import config



api_token = '68e6b02857aa41cfa2ffd3cd371e4151'
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json

updater = Updater(config.token) # Токен API к Telegram
dispatcher = updater.dispatcher

# updater = Updater(config.token) # Токен API к Telegram
# dispatcher = updater.dispatcher
# print (dispatcher.chat_data)
# # Обработка команд
# def startCommand(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
# def textMessage(bot, update):
#     response = 'Получил Ваше сообщение: ' + update.message.text
#     bot.send_message(chat_id=update.message.chat_id, text=response)

# Хендлеры
# start_command_handler = CommandHandler('start', startCommand)
# text_message_handler = MessageHandler(Filters.text, textMessage)

# # Добавляем хендлеры в диспетчер
# dispatcher.add_handler(start_command_handler)
# dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
# updater.start_polling(clean=True)


# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')

def textMessage(bot, update):
    request = apiai.ApiAI(api_token).text_request()  # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()