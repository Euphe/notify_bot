import logging
import telegram
from telegram.ext import Updater
import random
import uuid
import threading
import server
import storage
from logging.handlers import TimedRotatingFileHandler
import os
import sys
import server_settings
class NotifyBot(object):
    def __init__(self, api, updater = None):
        self.api = api
        self.updater = updater

        self.help_text = "Use /key to get a key, then use it in your app to get notifications here."
        self.commands = [
            ('start', self.start),
            ('key', self.key),
            ('help', self.help),
            ('server', self.get_host_name)
        ]

        #self.keys = {} #"key" : "chat_id"
        self.updater_thread = None
        self.server_thread = None


    """ commands """
    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Hello, I generate unique keys and send you notifications!")

    def unknown(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def error(self, bot, update, error):
        logger.debug('Update %s caused error %s' % (update, error))

    def key(self, bot, update):
        key = self.generate_key()
        bot.sendMessage(chat_id=update.message.chat_id, text=key)
        #self.keys[key] = update.message.chat_id
        storage.add_key(key, update.message.chat_id)
        bot.sendMessage(chat_id=update.message.chat_id, text="Your key has been registered!")

    def get_host_name(self, bot, update):
        name = server.get_server_name()
        bot.sendMessage(chat_id=update.message.chat_id, text="Notify bot receives notifications on:")
        bot.sendMessage(chat_id=update.message.chat_id, text=name)

    def help(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=self.help_text)
        bot.sendMessage(chat_id=update.message.chat_id, text="Notify Bot is receiving messages on:\nhttp://%s/<your_key>"%(server_settings.SERVER_NAME))
        try:
            #logger.debug(key_from_value(self.keys, update.message.chat_id))
            #key = key_from_value(self.keys, update.message.chat_id)
            key = storage.get_key(update.message.chat_id)
            if not key:
                raise(Exception("No key"))
            bot.sendMessage(chat_id=update.message.chat_id, text="Your registered key is:\n%s"%(key))

            bot.sendMessage(chat_id=update.message.chat_id, text="Send any text in 'text' attribute of a POST request to this link:\nhttp://%s/%s\n... and I will send it to you."%(server_settings.SERVER_NAME, key))
        except:
            bot.sendMessage(chat_id=update.message.chat_id, text="You have no keys. Use /key to generate one.")

        bot.sendMessage(chat_id=update.message.chat_id, text="Still confused? See the readme:\nhttps://github.com/Euphe/notify_bot/blob/master/README.md")

    

    """ bot operation functions """
    def send_notification(self, key, text):
        try:
            chat_id = storage.get_chat_id(key)
            if not chat_id:
                raise(Exception("No chat id"))
            self.api.sendMessage(chat_id=chat_id, text=text)
            return 1
        except:
            logger.debug("Key not found")
            return 0

    def generate_key(self):
        return str(uuid.uuid1())

    def map_commands(self):
        for command in self.commands:
            self.updater.dispatcher.addTelegramCommandHandler(command[0], command[1])
        self.updater.dispatcher.addUnknownTelegramCommandHandler(self.unknown)
        self.updater.dispatcher.addTelegramMessageHandler(self.unknown)
        self.updater.dispatcher.addErrorHandler(self.error)

    def run(self):
        self.map_commands()
        #self.updater.start_polling(poll_interval=0.1, timeout=10)

        def start_server():
            server.run_server(self)

        def start_updater(poll_interval, timeout):
            self.updater.start_polling(poll_interval=poll_interval, timeout=timeout)
            self.updater.idle()

        self.server_thread = threading.Thread(target=start_server)
        self.server_thread.daemon = True 

        args = (0.1, 10)
        self.updater_thread = threading.Thread(target=start_updater, args=args)
        self.updater_thread.daemon = True

        self.server_thread.start()
        self.updater_thread.start()
        
        while(True):
            pass

abs_path = os.path.dirname(os.path.realpath(sys.argv[0]))
log_path = abs_path+'/logs/'
if not os.path.exists( log_path ):
    os.makedirs(log_path)

log_file = log_path+'debug.log'
fh = TimedRotatingFileHandler(log_file, when="d", interval = 1, backupCount = 5)
fh.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger.addHandler(fh)

with open("api.token") as f:
    token = f.read().strip()

notify_bot = NotifyBot(telegram.Bot(token=token), updater = Updater(token=token))
notify_bot.run()