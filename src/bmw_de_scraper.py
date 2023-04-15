from selenium import webdriver
from lxml import etree
import json
from car import Car
from datetime import datetime

def parse_product_div(product, tree):
    props = product.xpath("./@data-prop")[0]

    # brand
    brand = "BMW"

    # model
    model = "M340i"

    # product code
    props = props.replace("'", '"').replace("container", '"container"').replace("productCode", '"productCode"')
    props = json.loads(props)
    product_code = props['productCode']

    # url
    url = "https://gebrauchtwagen.bmw.de/nsc/Fahrzeuge/BMW/3er/340/M340i-xDrive-Limousine/p/" + product_code

    # registration
    registration = tree.xpath(f'//*[@id="buyTab_{product_code}"]/ul/li[1]/div/span[2]/span/text()')[0]

    # km
    km = tree.xpath(f'//*[@id="buyTab_{product_code}"]/ul/li[3]/div/span[2]/span/text()')[0]

    # price
    # search in product for a div with class "price-inner"
    # get text
    price_list = product.xpath('.//div[@class="price-inner"]/span[1]/text()')
    if len(price_list) != 2:
        # vat not deductible
        return None
    price = price_list[0].strip()
    price_float = float(price.split('\xa0')[0].replace(".", "").replace(",", "."))
    if price_float > 55000:
        # price too low
        return None

    # date added - now
    date_added = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # avatar
    source = product.xpath(f'.//*[@class="image-content"]/a/picture/source[1]')
    avatar = source[0].xpath("./@srcset")[0].split(" ")[0]

    # create car
    car = Car(brand, model, registration, km, price, url, product_code, date_added, avatar)

    return car

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized");
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options
    )

    return driver

def scrape():
    driver = get_driver()

    cars = []

    try:
        driver.get("https://gebrauchtwagen.bmw.de/nsc/search?q=%3Arelevance%3ApriceValueRange%3A%253C%252060.000%2520%25E2%2582%25AC%3Acondition-mileageRange%3A%253C%252070%2C000%2520km%3A%3AcreationDateSort-asc%3Aattributes-bodyType%3ALimousine%3A%3AcreationDateSort-asc%3Aseries%3A3%3A%3AcreationDateSort-asc%3Amodel%3A340%3A%3AcreationDateSort-asc%3Aenvironment-fuelType%3ABenzin&searchId=")
        
        # get html and load it in lxml
        html = driver.page_source
        tree = etree.HTML(html)

        # search element with class "h1-result-count"
        # get "data-count" attribute
        # convert to int
        count = int(tree.xpath("//h1[@class='h1-result-count']/@data-count")[0])

        # get div with class "product__listing product__grid row"
        # get all divs inside
        container = tree.xpath("//div[@class='product__listing product__grid row']/div")

        # loop through all divs
        for div in container:
            # get first's div "data-prop" attribute
            product = div.xpath("./div")[0]
            car = parse_product_div(product, tree)

            # append car to list
            if car != None:
                cars.append(car)
        
    except Exception as e:
        print("Error")
        print(e)
    finally:
        driver.quit()

        return cars

def get_features(url):
    driver = get_driver()

    features = []

    try:
        driver.get(url)

        # get html and load it in lxml
        html = driver.page_source
        tree = etree.HTML(html)

        equipment = tree.xpath("//div[@class='equipment']//span/text()")

        features = equipment
    except Exception as e:
        print("Error")
        print(e)
    finally:
        driver.quit()
        return features