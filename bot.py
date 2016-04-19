import logging
import telegram
from telegram.ext import Updater
import random
import uuid
import threading
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
class NotifyBot(object):
    def __init__(self, api, updater = None):
        self.api = api
        self.updater = updater

        self.help_text = "Use /key to get a key, then use it in your app to get notifications here."
        self.commands = [
            ('start', self.start),
            ('key', self.key),
            ('help', self.help),
        ]

        self.updater_thread = None


    """ commands """
    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I generate unique keys and send you notifications!")

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def error(self, bot, update, error):
        logger.debug('Update %s caused error %s' % (update, error))

    def key(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=self.generate_key())

    def help(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=self.help_text)

    def generate_key(self):
        return str(uuid.uuid1())

    """ bot operation functions """
    def map_commands(self):
        for command in self.commands:
            self.updater.dispatcher.addTelegramCommandHandler(command[0], command[1])
        self.updater.dispatcher.addUnknownTelegramCommandHandler(self.unknown)
        self.updater.dispatcher.addTelegramMessageHandler(self.unknown)
        self.updater.dispatcher.addErrorHandler(self.error)



    def run(self):
        self.map_commands()
        #self.updater.start_polling(poll_interval=0.1, timeout=10)

        def start_updater(poll_interval, timeout):
            self.updater.start_polling(poll_interval=poll_interval, timeout=timeout)
            self.updater.idle()

        args = (0.1, 10)
        self.updater_thread = threading.Thread(target=start_updater, args=args)
        self.updater_thread.daemon = True
        self.updater_thread.start()
        
        while(True):
            pass
        

    def stop(self):
        self.updater.stop()


    



with open("api.token") as f:
    token = f.read().strip()

notify_bot = NotifyBot(telegram.Bot(token=token), updater = Updater(token=token))

notify_bot.run()