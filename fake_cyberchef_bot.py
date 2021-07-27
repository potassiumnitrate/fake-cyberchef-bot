'''
from flask import Flask, request
from telebot.credentials import token, bot_username
'''
# initialize bot ---------------------------------------------------------------------------------------------------------------------------------------------------
# import everything
#import telegram
import telebot
import logging
from uuid import uuid4
#from telebot import types
from datetime import datetime
#from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent
#from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler
#from telegram.utils.helpers import escape_markdown

import base64
import qrcode
from io import BytesIO

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

token = "1925350189:AAGAdlsxBUr2iCSRF1ZpegJst45p0lUdQvE"
bot = telebot.TeleBot(token)
#bot.send_message(message.chat.id,'Hello!')

# date & time format
format_ = "%d-%m-%Y %H%M"

# commands ---------------------------------------------------------------------------------------------------------------------------------------------------------
# command - /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
        "Fake Cyberchef Bot\n" +
        "Based on GCHQ Cyberchef https://github.com/gchq/CyberChef \n"
        "Use the tool here https://gchq.github.io/CyberChef/")

# command - /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 
        "Commands:\n" + 
        "1. /start - Description\n" + 
        "2. /help  - This message\n" + 
        "3. /tobase64 <type your own message> \n" +
        "4. /frombase64 <type your own base64 message> \n" +
        "5. /generateQR <type your own message>")

# command - /tobase64
@bot.message_handler(commands=['tobase64'])
def tobase64(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        string.isascii()
        string_bytes = string.encode('ascii')
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode('ascii')
            
    except ValueError:
        bot.reply_to(message, 
                "Invalid value.\n" + 
                "Try again.")
    else:
        bot.reply_to(message, base64_string)

# command - /frombase64
@bot.message_handler(commands=['frombase64'])
def frombase64(message):
    try:
        base64_string = str(message.text)
        if not base64_string:
            raise ValueError
        base64_string = str(message.text).split(" ", 1)[1]
        base64_string.isascii()
        base64_bytes = base64_string.encode('ascii')
        string_bytes = base64.b64decode(base64_bytes)
        string = string_bytes.decode('ascii')
    except ValueError:
        bot.reply_to(message, 
                "Invalid value.\n" + 
                "Try again.")
    else: 
        bot.reply_to(message, string)

# command - /generateQR
@bot.message_handler(commands=['generateQR'])
def generateQR(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        img = qrcode.make(string)
    except:
        bot.reply_to(message,
                "Unknown error.")
    else:
        bio = BytesIO()
        bio.name = "qrcode.jpeg"
        img.save(bio, 'JPEG')
        bio.seek(0)
        bot.send_photo(message.chat.id, photo=bio)
        # bot.reply_to(message, img)

# query handler ----------------------------------------------------------------------------------------------------------------------------------------------------

'''@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text = "Answer processing...")
    answer = "You replied no.\nWhyyyyy :-("
    if call.data == '0':
        answer = "You replied yes.\nYay! :-D"

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
'''

bot.polling()