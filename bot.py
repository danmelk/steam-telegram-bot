from operator import imod
import telegram
import os
from dotenv import load_dotenv
load_dotenv()
TOCKEN = os.getenv('TOCKEN')

from telegram.ext import Updater
updater = Updater(token=TOCKEN, use_context=True)