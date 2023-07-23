import discord
from discord.ext import commands, tasks
import asyncio
import time
import json

class LoopRatioCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.data = self.bot.tools.load_json(self.bot.tools.path_loops+"ratios.json")

    
    @tasks.loop(seconds=1)
    async def ratio_loop(self):
        delete_ratio = []
        for ratio in self.data.items():
            if time.time() - ratio[1]["start"] >= 10:
                delete_ratio.append(ratio[0])
                try:
                    channel = self.bot.get_channel(ratio[1]["channel"])
                    user = self.bot.get_user(ratio[1]["author"])
                    message: discord.Message = await channel.fetch_message(ratio[1]["message"])
                    yes = 0
                    no = 0
                    for react in message.reactions:
                        if react.emoji == "✅":
                            yes += react.count - int(react.me)
                        elif react.emoji == "❌":
                            no += react.count - int(react.me)
                    if no >= yes:
                        await channel.send(f"Gros flop pour <@{user.id}> tu gagnes le rôle de floppeur, cheh!")
                        guild = channel.guild
                        roles = await guild.fetch_roles()
                        role = None
                        for r in roles:
                            if r.name == "floppeur" and r.is_assignable():
                                role = r
                        if role is None:
                            role = await guild.create_role(name="floppeur", permissions=discord.Permissions(), colour=discord.Colour.blurple(), hoist=True, mentionable=True)
                        member = guild.get_member(user.id)
                        await member.add_roles(role)
                                
                    else:
                        await channel.send(f"Gros ratio de la part de <@{user.id}>, cheh!")
                except Exception as e:
                    print(e)
        for r in delete_ratio:
            del self.data[r]
        self.save_data()
    
    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        self.ratio_loop.start()
    
    def save_data(self):
        self.bot.tools.save_json(self.bot.tools.path_loops+"ratios.json", self.data)