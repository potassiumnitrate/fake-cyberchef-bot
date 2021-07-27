'''
from flask import Flask, request
from telebot.credentials import token, bot_username
'''
# initialize bot ---------------------------------------------------------------------------------------------------------------------------------------------------
# import everything 
import telegram
import telebot
import logging
from uuid import uuid4
#from telebot import types
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler
from telegram.utils.helpers import escape_markdown

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
        string = str(message.text).split(" ", 1)[1]
        if not string:
            raise ValueError
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
        base64_string = str(message.text).split(" ", 1)[1]
        if not base64_string:
            raise ValueError
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
        string = str(message.text).split(" ", 1)[1]
        if not string:
            raise ValueError
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

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text = "Answer processing...")
    answer = "You replied no.\nWhyyyyy :-("
    if call.data == '0':
        answer = "You replied yes.\nYay! :-D"

    bot.send_message(call.message.chat.id, answer)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
'''
@bot.inline_handler(func=lambda query: True)
def inlinequery(inline_query):
    results = [InlineQueryResultArticle(
        id = uuid4(),
        title = '/datetime',
        input_message_content = InputTextMessageContent(
            message_text='/datetime'
        ))]
    bot.answer_inline_query(inline_query.id, results = results)

def main():
    updater = Updater(token, use_context = True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inlinequery))
    dp.add_error_handler(ValueError)
    
    updater.start_polling()
    updater.idle()

main()

def inlinequery(update, context):
    # Handle the inline query.
    query = update.inline_query.query
    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="/start",
            input_message_content=InputTextMessageContent(
                query.upper())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="/help",
            input_message_content=InputTextMessageContent(
                "*{}*".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),
        InlineQueryResultArticle(
            id=uuid4(),
            title="/datetime",
            input_message_content=InputTextMessageContent(
                "_{}_".format(escape_markdown(query)),
                parse_mode=ParseMode.MARKDOWN)),    
        ]

    update.inline_query.answer(results)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
'''
bot.polling()