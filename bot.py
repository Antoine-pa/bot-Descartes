import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from os import getenv

import cogs.admin
import cogs.event
import cogs.loops.ratio
import cogs.math
import cogs.poll
import cogs.tournament
import cogs.troll
import cogs.archive

PREFIX='!:'

cogs = [
    cogs.admin.AdminCog,
    cogs.event.EventCog,
    cogs.loops.ratio.RatioCog,
    cogs.math.MathCog,
    cogs.poll.PollCog,
    cogs.tournament.TournamentCog,
    cogs.troll.TrollCog,
    cogs.archive.ArchiveCog,
]

class Bot(commands.Bot):
    def __init__(self):
        load_dotenv()
        self.guild = discord.Object(getenv('GUILD'))
        super().__init__(command_prefix='!:', help_command=None, intents=discord.Intents.all())

    async def setup_hook(self):
        for cog in cogs:
            await self.add_cog(cog(self))
        await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as{self.user} ({self.user.id})')
        
