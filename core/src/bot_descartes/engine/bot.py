import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from .cogs import *
from .utils import *

class Bot(commands.Bot):
    def __init__(self):
        self.guild = discord.Object("1115733653323001957")
        self.tools = Tools()
        self.loop_ratio_cog = LoopRatioCog(self)
        super().__init__(command_prefix="!:", help_command=None, intents=discord.Intents.all())
    
    async def setup_hook(self):
        await self.add_cog(TrollCog(self))
        await self.add_cog(EventCog(self))
        await self.add_cog(AdministrationCog(self))
        await self.add_cog(MathsCog(self))
        await self.add_cog(self.loop_ratio_cog)
        await self.tree.sync()
    
    async def on_ready(self):
        print(f'Logged in as {self.user}') #Bot Name
        print(self.user.id) #Bot ID
