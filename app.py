import telegram
from telegram.ext import Updater
from bot import NotifyBot

with open("api.token") as f:
    token = f.read().strip()

application = NotifyBot(telegram.Bot(token=token), updater = Updater(token=token))
#notify_bot.run()