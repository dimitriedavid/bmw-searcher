class Car:
    def __init__(self, brand, model, registration, km, price, url, product_code, date_added, avatar):
        self.brand = brand
        self.model = model
        self.registration = registration
        self.km = km
        self.price = price
        self.url = url
        self.product_code = product_code
        self.date_added = date_added
        self.avatar = avatar

    def get_dict(self):
        return {
            "brand": self.brand,
            "model": self.model,
            "registration": self.registration,
            "km": self.km,
            "price": self.price,
            "url": self.url,
            "product_code": self.product_code,
            "date_added": self.date_added,
            "avatar": self.avatar
        }

    def get_text_message(self):
        return f"""<b>{self.brand} {self.model}</b>
<b>Registration:</b> {self.registration}
<b>Kilometers:</b> {self.km}
<b>Price:</b> {self.price}
<b>URL:</b> {self.url}
"""


def get_car_from_dict(car_dict):
    return Car(
        car_dict["brand"],
        car_dict["model"],
        car_dict["registration"],
        car_dict["km"],
        car_dict["price"],
        car_dict["url"],
        car_dict["product_code"],
        car_dict["date_added"],
        car_dict["avatar"]
    )
