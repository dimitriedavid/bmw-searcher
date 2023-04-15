from bot import TelegramBot
from config import telegram_token, chat_id
import pymongo
from bmw_de_scraper import scrape, get_features
from car import get_car_from_dict
import time
from datetime import datetime

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
    price_changes = 0
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
        else:
            # check if price changed
            old_car = collection.find_one({"product_code": car.product_code})
            if old_car["price"] != car.price:
                # send message
                tgmBot.send_price_change(car, old_car["price"])

                # update car in db
                collection.update_one({"product_code": car.product_code}, {"$set": car.get_dict()})
                price_changes += 1

    sold_cars = 0
    # check if any car was sold
    for car in collection.find():
        if not any(c.product_code == car["product_code"] for c in cars) and car["sold"] is None:
            # send message
            tgmBot.send_car_sold(get_car_from_dict(car))

            # mark car as sold with timestamp
            collection.update_one({"product_code": car["product_code"]}, {"$set": {"sold": datetime.now().strftime("%d.%m.%Y %H:%M:%S")}})

            sold_cars += 1

    print(f"Found {new_cars} new cars")
    print(f"Found {sold_cars} sold cars")
    print(f"Found {price_changes} price changes")

    # send daily update
    daily_collection = client["m340i"]["daily"]
    last_daily = daily_collection.find_one({"name": "last_daily"})
    # if no last_daily entry exists, create one
    if last_daily is None:
        daily_collection.insert_one({"name": "last_daily", "value": 0})
        last_daily = 0
    else:
        last_daily = last_daily["value"]
    if time.time() - last_daily > 24 * 60 * 60:
        daily_collection.update_one({"name": "last_daily"}, {"$set": {"value": time.time()}})
        tgmBot.send_daily(new_cars, sold_cars, price_changes, len(cars))

if __name__ == '__main__':
    # run every 5 minutes
    while True:
        print("Running... time is {}".format(time.ctime()))
        main()
        time.sleep(5 * 60)