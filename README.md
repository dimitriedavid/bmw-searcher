# Telegram bot for updating BMW M340i stock from bmw.de website

## Prerequisites
* docker
* docker-compose
* pm2
* python3

## Installation
1. Clone the repository
2. Install dependencies
```sh
pip3 install -r requirements.txt
```

## Configuration
1. Create a bot using BotFather and get the token
2. Create a file `src/config.py` with the following content:
```py
telegram_token = 'TELEGRAM_TOKEN'
chat_id = 'CHAT_ID'
```

## Run
1. Start database and Selenium web driver
```sh
docker compose -f docker/docker-compose.yml up -d
```
2. Start the bot
```sh
pm2 start src/main.py --name bmw-scraper --interpreter python3 --watch
```

## License
[MIT](LICENSE)