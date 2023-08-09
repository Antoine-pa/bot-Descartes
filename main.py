from bot import Bot
from dotenv import load_dotenv
from os import getenv

load_dotenv()
TOKEN = getenv('TOKEN')

if __name__ == '__main__':
    Bot().run(TOKEN)
