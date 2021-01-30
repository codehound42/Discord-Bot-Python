import bot
import requests
from bs4 import BeautifulSoup
import dotenv
import os


# Load .env variables
dotenv.load_dotenv()

BATTLEMETRICS_HYPIXEL_URL = "https://www.battlemetrics.com/servers/minecraft/5873087"
BATTLEMETRICS_HYPIXEL_DIV_CLASS = "col-md-6 server-info"


def check_server_population(server_name: str, url: str, div_class: str):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    player_count = soup.find('div', class_=div_class).find_all('dd')[2].text
    string_to_output = f"Current server population on {server_name}: **{player_count}**"
    bot.post_data_to_webhook(os.getenv('GENERAL_CHAT_WEBHOOK'), string_to_output)


if __name__ == "__main__":
    check_server_population("Hypixel Network", BATTLEMETRICS_HYPIXEL_URL, BATTLEMETRICS_HYPIXEL_DIV_CLASS)