__author__ = 'Mikhail'
# -*- coding: utf-8 -*-
import config
import telebot
import vk_parser
from telebot import types


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(u'Расписание', u'Стоимость', u'Адрес клуба', u'День борьбы')
    bot.send_message(message.chat.id, u'Привет, я бот команды по БЖЖ Ronin Family', reply_markup=markup)
    f = open('chat_ids.txt', 'w')
    f.write(str(message.chat.id) + '\n')
    f.close()


@bot.message_handler(func=lambda m: True)
def reply_to_user(message):
    if message.text == u'Расписание':
        bot.send_message(message.chat.id, vk_parser.get_schedule())
        bot.send_photo(message.chat.id, vk_parser.get_schedule_photo())
    elif message.text == u'Стоимость':
        bot.send_message(message.chat.id, "Under Construction"
                                          "")


@bot.message_handler(commands=['ronin'])
def send_auth(message):
    text = vk_parser.get_last_post('roninfamily')
    bot.send_message(message.chat.id, text)

bot.polling()

