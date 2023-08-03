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
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        pass
        #voir si le message était un sondage pour éventuellement le supprimer
        #de même pour un ratio
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload:discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.message_id) in self.bot.polls_cog.data_polls:
            list_react_color = self.bot.tools.list_react_color[:len(self.bot.polls_cog.data_polls[str(payload.message_id)]["choices"])]
            if str(payload.emoji) in list_react_color:
                #réponse à un sondage :
                message = await self.bot.tools.get_message(self.bot, payload.channel_id, payload.message_id)
                await self.bot.polls_cog.update_poll(message, list_react_color.index(str(payload.emoji)), 1)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload:discord.RawReactionActionEvent):
        if payload.user_id == self.bot.user.id:
            return
        if str(payload.message_id) in self.bot.polls_cog.data_polls:
            list_react_color = self.bot.tools.list_react_color[:len(self.bot.polls_cog.data_polls[str(payload.message_id)]["choices"])]
            if str(payload.emoji) in list_react_color:
                message = await self.bot.tools.get_message(self.bot, payload.channel_id, payload.message_id)
                await self.bot.polls_cog.update_poll(message, list_react_color.index(str(payload.emoji)), -1)