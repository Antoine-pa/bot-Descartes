import discord
from discord.ext import commands
from discord import app_commands
from .commands import *

class Bot(commands.Bot):
    def __init__(self):
        self.guild = discord.Object("1115733653323001957")
        super().__init__(command_prefix="!:", help_command=None, intents=discord.Intents.all())
    
    async def setup_hook(self):
        await self.add_cog(SlashCommands(self))
        await self.tree.sync()
    
    async def on_ready(self):
        print(f'Logged in as {self.user}') #Bot Name
        print(self.user.id) #Bot ID