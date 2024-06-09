import telebot

from credential import Credential


class Telegram:
    def __init__(self):
        self.token = Credential().get_telegram_token()
        self.channel_id = Credential().get_channel_id()
        self.bot = telebot.TeleBot(self.token)

    def send_message(self, message):
        self.bot.send_message(self.channel_id, message)
