from engine import Bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

Bot().run(TOKEN)
