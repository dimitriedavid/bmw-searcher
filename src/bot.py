import telebot
from car import Car
import time

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
            print("Sending car: {}".format(car.get_text_message()))
        else:
            self.bot.send_photo(self.chat_id, car.avatar)
            self.bot.send_message(self.chat_id, car.get_text_message(), parse_mode="HTML")

    def send_car_sold(self, car: Car):
        if self.mock:
            print("Sending car sold: {}".format(car.get_text_message()))
        else:
            self.bot.send_photo(self.chat_id, car.avatar)
            self.bot.send_message(self.chat_id, "⛔⛔Car sold⛔⛔\n{}⛔⛔Car sold⛔⛔".format(car.get_text_message()), parse_mode="HTML")

    def send_price_change(self, car: Car, old_price):
        if self.mock:
            print("Sending price change: {}".format(car.get_text_message()))
        else:
            self.bot.send_photo(self.chat_id, car.avatar)
            self.bot.send_message(self.chat_id, f"💰💰Price change💰💰\n<b>Old price: {old_price}</b>\n\n{car.get_text_message()}", parse_mode="HTML")

    def send_daily(self, new_cars, sold_cars, price_changes, stock):
        if self.mock:
            print("Daily update: {}".format(f"Found {new_cars} new cars\nFound {sold_cars} sold cars\nFound {price_changes} price changes"))
        else:
            self.bot.send_message(self.chat_id, f"Daily update:\nStock is {stock} cars\nFound {new_cars} new cars\nFound {sold_cars} sold cars\nFound {price_changes} price changes")