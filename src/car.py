from difflib import SequenceMatcher

class Car:
    def __init__(self, brand, model, registration, km, price, url, product_code, date_added, avatar, features=None):
        self.brand = brand
        self.model = model
        self.registration = registration
        self.km = km
        self.price = price
        self.url = url
        self.product_code = product_code
        self.date_added = date_added
        self.avatar = avatar
        self.features = features

    def add_features(self, features):
        self.features = features

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
            "avatar": self.avatar,
            "features": self.features
        }

    def get_text_message(self):
        return f"""<b>{self.brand} {self.model}</b>
<b>Registration:</b> {self.registration}
<b>Kilometers:</b> {self.km}
<b>Price:</b> {self.price}
<b>URL:</b> {self.url}
<b>Filtered features:</b> {get_features_text(self.features)}
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
        car_dict["avatar"],
        car_dict["features"]
    )

def get_features_text(features):
    selected_features = []
    interesting_features = ['Driving Assistant Professional', 'M Technik Paket', 'Glasdach, elektrisch mit Schiebe- und Hebefunktion', "Sitzverstellung, elektrisch mit Memory für Fahrersitz"]
    diff_threshold = 0.8

    for feature in features:
        for interesting_feature in interesting_features:
            if SequenceMatcher(None, feature, interesting_feature).ratio() > diff_threshold:
                selected_features.append(feature)
                break

    black_list = ['M Aerodynamikpaket']
    selected_features = [feature for feature in selected_features if feature not in black_list]

    text = "\n"
    for feature in selected_features:
        if feature == "M Technik Paket":
            text += f"✅{feature}\n"
            continue
        if feature == "Driving Assistant Professional":
            text += f"✅{feature}\n"
            continue
        if feature == "Glasdach, elektrisch mit Schiebe- und Hebefunktion":
            text += f"✅Sunroof\n"
            continue
        if feature == "Sitzverstellung, elektrisch mit Memory für Fahrersitz":
            text += f"✅Electric seats\n"
            continue
        text += f"{feature}\n"

    return text