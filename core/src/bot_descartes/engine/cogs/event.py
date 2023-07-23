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
        if content == "ratio" or " ratio " in content or content.startswith("ratio ") or content.endswith(" ratio") or (content[:-1].endswith(" ratio") and (not 97 <= ord(content[-1]) <= 122)):
            resp: discord.Message = await message.channel.send("Voulez vous faire un ratio?")

            def check_react_ratio(reaction, user):
                return message.author.id == user.id and resp.id == reaction.message.id and (str(reaction.emoji) in ("✅", "❌"))

            await resp.add_reaction("✅")
            await resp.add_reaction("❌")

            try:
                reaction, _ = await self.bot.wait_for("reaction_add", timeout = 10, check = check_react_ratio)
            except:
                resp2: discord.Message = await message.channel.send("ratio annulé")
                await resp.delete()
                await resp2.delete(delay=10)
                return
            if str(reaction) == "✅":
                if str(message.author.id) + str(message.channel.id) in self.bot.loop_ratio_cog.data:
                    resp: discord.Message = await message.channel.send("Vous faites déjà un ratio dans ce salon.")
                    await resp.delete(delay=10)
                    return
                await message.add_reaction("✅")
                await message.add_reaction("❌")
                self.bot.loop_ratio_cog.data[str(message.author.id) + str(message.channel.id)] = {"start" : time.time(), "channel" : message.channel.id, "author" : message.author.id, "message" : message.id}
                self.bot.loop_ratio_cog.save_data()
                await message.channel.send("Un ratio est lancé! Il se finira dans 10min.")
            await resp.delete()