from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
from config import PATHS
from dotenv import load_dotenv
from os import getenv
from utils import write_json, read_json

load_dotenv()

path_archives = f'{PATHS["storage"]}/{getenv("ARCHIVES_STORAGE")}'

class ArchiveCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.data_archives = read_json(path_archives)