import os
import json
from warnings import filters
from telegram import Update, TelegramObject, MessageEntity
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters
import logging
from dotenv import load_dotenv
load_dotenv()
channel_url = '@steam_new_releases'


from scrapper import steam_scrape

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "Beep boop, I'm a bot!") 

def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def channel(update: Update, context: CallbackContext):
    game_data = steam_scrape()

    for entry in game_data[0:5]:
        # for dictElement in entry:
        # for eachStr in entry['review']:
        #     merged = ratingData 
        if entry['discount'] == 'None':
            message = f"Link -> {entry['link']}\nTitle -> {entry['title']}\nPrice -> {entry['price']}\nPlatform -> {entry['platform']}\nRating -> {entry['review']}\nDate -> {entry['date']}"
        else:
            message = f"Link -> {entry['link']}\nTitle -> {entry['title']}\nPrice -> {entry['price']}\nPlatform -> {entry['platform']}\nRating -> {entry['review']}\nDate -> {entry['date']}"
        
        context.bot.send_message(chat_id = channel_url, text = message)


def main():
    TOKEN = os.getenv('TOKEN')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    caps_handler = CommandHandler('caps', caps)
    start_handler = CommandHandler(['start', 'help'], start)
    data_handler = CommandHandler('data', channel)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(data_handler)


    updater.start_polling()

if __name__ == '__main__':
    main()