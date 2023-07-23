import discord
from discord.ext import commands
import time

class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        content = " " + message.content.lower()
        if content == " ratio" or " ratio " in content or content.startswith("ratio ") or content.endswith(" ratio") or (content[:-1].endswith(" ratio") and (not 97 <= ord(content[-1]) <= 122)):
            await self.bot.loop_ratio_cog.create_ratio(message)