from bot import TelegramBot
from config import telegram_token, chat_id
import pymongo
from bmw_de_scraper import scrape, get_features
from car import get_car_from_dict
import time

def main():
    # init telegram bot
    tgmBot = TelegramBot(telegram_token, mock=False)
    tgmBot.set_chat_id(chat_id)

    # init mongo db
    client = pymongo.MongoClient("mongodb://root:example@localhost:27017/")
    
    # check if db exists
    collection = client["m340i"]["bmw_de"]
    
    # get all cars
    cars = scrape()

    print(f"Found {len(cars)} cars")

    new_cars = 0
    for car in cars:
        # check if car is already in db
        if collection.count_documents({"product_code": car.product_code}) == 0:
            # get features
            car.add_features(get_features(car.url))

            # send message
            tgmBot.send_car(car)

            # add car to db
            collection.insert_one(car.get_dict())

            new_cars += 1
            time.sleep(5)

    print(f"Found {new_cars} new cars")

if __name__ == '__main__':
    main()