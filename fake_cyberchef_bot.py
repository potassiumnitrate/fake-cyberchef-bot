# initialize bot ---------------------------------------------------------------------------------------------------------------------------------------------------
# import everything
import telebot
import logging

import base64
import codecs
import qrcode
from io import BytesIO
import os
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Get token from heroku
token = os.environ["token"]

bot = telebot.TeleBot(token)

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

# command - /todec
@bot.message_handler(commands=['todec'])
def todec(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        string.isascii()
        string = str([ord(i) for i in string]).strip("[]").replace(",","")
    except ValueError:
        bot.reply_to(message,
                     "Invalid value.\n" +
                     "Try again.")
    else:
        bot.reply_to(message, string)

# command - /fromdec
@bot.message_handler(commands=['fromdec'])
def fromdec(message):
    try:
        string = str(message.text)
        if not string and re.match("^[0-9 ]+$", string):
            raise ValueError
        arr = [int(i) for i in string.split()]
        string = str(message.text).split(" ", 1)[1]
        string = "".join([chr(i) for i in string])
    except ValueError:
        bot.reply_to(message,
                     "Invalid value.\n" +
                     "Try again.")
    else:
        bot.reply_to(message, string)

# command - /tohex
@bot.message_handler(commands=['tohex'])
def tohex(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        string.isascii()
        string_bytes = string.encode('ascii')
        base16_bytes = base64.b16decode(string_bytes)
        base16_string = base16_bytes.decode('ascii')
        base16_string = " ".join([base16_string[i:i+2] for i in range(0, len(base16_string), 2)])
    except ValueError:
        bot.reply_to(message,
                     "Invalid value.\n" +
                     "Try again.")
    else:
        bot.reply_to(message, base16_string)

# command - /fromhex
@bot.message_handler(commands=['fromhex'])
def fromhex(message):
    try:
        base16_string = str(message.text)
        if not base16_string:
            raise ValueError
        base16_string = str(message.text).split(" ", 1)[1]
        base16_string.isascii()
        base16_bytes = base16_string.encode('ascii')
        string_bytes = base64.b16decode(base16_bytes)
        string = string_bytes.decode('ascii')
    except ValueError:
        bot.reply_to(message,
                     "Invalid value.\n" +
                     "Try again.")
    else:
        bot.reply_to(message, string)

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

# command - /encoderot13
@bot.message_handler(commands=['encoderot13'])
def encoderot13(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        string.isascii()
        string = codecs.encode(string, 'rot_13')
    except ValueError:
        bot.reply_to(message,
                "Invalid value.\n" +
                "Try again.")
    else:
        bot.reply_to(message, string)

# command - /decoderot13
@bot.message_handler(commands=['decoderot13'])
def decoderot13(message):
    try:
        string = str(message.text)
        if not string:
            raise ValueError
        string = str(message.text).split(" ", 1)[1]
        string.isascii()
        string = codecs.decode(string, 'rot_13')
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

bot.polling()