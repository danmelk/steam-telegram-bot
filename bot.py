from multiprocessing import context
import os
from warnings import filters
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
import logging
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


from scrapper import steam_scrape

def start(update: Update, context: CallbackContext):
    
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Beep boop I'm a bot.") 

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def data(update: Update, context: CallbackContext):
    pass


def main():
    TOKEN = os.getenv('TOKEN')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(start_handler)


    updater.start_polling()

if __name__ == '__main__':
    main()