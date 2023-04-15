import telebot
from car import Car

class TelegramBot:
    def __init__(self, token, mock=False):
        self.token = token
        self.bot = telebot.TeleBot(token)
        self.mock = mock
    
    def set_chat_id(self, chat_id):
        self.chat_id = chat_id

    def send_text_message(self, message, parse_mode=None):
        if self.mock:
            print("Sending message: {}".format(message))
        else:
            self.bot.send_message(self.chat_id, message, parse_mode=parse_mode)

    def send_car(self, car: Car):
        if self.mock:
            print("Sending car: {}".format(car))
        else:
            self.bot.send_photo(self.chat_id, car.avatar, caption=car.get_text_message(), parse_mode="HTML")