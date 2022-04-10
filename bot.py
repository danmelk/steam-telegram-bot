import os
import json
from warnings import filters
import telegram
from telegram.constants import MESSAGEENTITY_ALL_TYPES
from telegram import MessageEntity, ParseMode, Update, TelegramObject
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
        reviewStr = entry['review']
        mergedReview = f"{reviewStr[0]}: {reviewStr[1]}"
        platformStr = entry['platform']
        if len(platformStr) == 2:
            mergedPlatform = f'{platformStr[0]}, {platformStr[1]}'
        else:
            mergedPlatform = f'{platformStr[0]}'
        if entry['discount'] == 'None':
            message = f"<b>Title</b> -> <a href='{entry['link']}'><b>{entry['title']}</b></a>\n<b>Price</b> -> {entry['price']}\n<b>Platform</b> -> {mergedPlatform}\n<b>Rating</b> -> {mergedReview}\n<b>Date</b> -> {entry['date']}"
        else:
            message = f"<b>Title</b> -> <a href='{entry['link']}'><b>{entry['title']}</b></a>\n<b>Price</b> -> <del>{entry['original-price']}</del> {entry['price']} ({entry['discount']})\n<b>Platform</b> -> {mergedPlatform}\n<b>Rating</b> -> {mergedReview}\n<b>Date</b> -> {entry['date']}"
        context.bot.send_message(chat_id = update.effective_chat.id, text = message, parse_mode = ParseMode.HTML)


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