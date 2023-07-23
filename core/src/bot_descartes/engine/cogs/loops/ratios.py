import discord
from discord.ext import commands, tasks
import asyncio
import time
import json

class LoopRatioCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.data_ratio = self.bot.tools.load_json(self.bot.tools.path_loops+"ratios.json")
        self.data_floppeurs = self.bot.tools.load_json(self.bot.tools.path_loops+"floppeurs.json")

    async def create_ratio(self, message):
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
            if str(message.author.id) + str(message.channel.id) in self.bot.loop_ratio_cog.data_ratio:
                resp: discord.Message = await message.channel.send("Vous faites déjà un ratio dans ce salon.")
                await resp.delete(delay=10)
                return
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            self.bot.loop_ratio_cog.data_ratio[str(message.author.id) + str(message.channel.id)] = {"start" : time.time(), "channel" : message.channel.id, "author" : message.author.id, "message" : message.id}
            self.bot.loop_ratio_cog.save_data_ratio()
            await message.channel.send("Un ratio est lancé! Il se finira dans 10min.")
        await resp.delete()

    
    @tasks.loop(seconds=1)
    async def ratio_loop(self):
        delete_ratio = []
        for ratio in self.data_ratio.items():
            if time.time() - ratio[1]["start"] >= 5:
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
                        key = str(member.id)+str(guild.id)
                        if key in self.data_floppeurs:
                            self.data_floppeurs[key]["start"] = time.time()
                        else:
                            self.data_floppeurs[key] = {"start": time.time(), "author" : member.id, "guild" : guild.id, "role" : role.id}
                        self.save_data_floppeurs()
                    else:
                        await channel.send(f"Gros ratio de la part de <@{user.id}>, cheh!")
                except Exception as e:
                    print(e)
        for r in delete_ratio:
            del self.data_ratio[r]
        self.save_data_ratio()
    
    @tasks.loop(seconds=1)
    async def floppeurs_loop(self):
        delete_flop = []
        for flop in self.data_floppeurs.items():
            if time.time() - flop[1]["start"] >= 5:
                delete_flop.append(flop[0])
                try:
                    guild = self.bot.get_guild(flop[1]["guild"])
                    member = guild.get_member(flop[1]["author"])
                    role = guild.get_role(flop[1]["role"])
                    await member.remove_roles(role)
                except Exception as e:
                    print(e)
        for f in delete_flop:
            del self.data_floppeurs[f]
        self.save_data_floppeurs()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        self.ratio_loop.start()
        self.floppeurs_loop.start()

    def save_data_ratio(self):
        self.bot.tools.save_json(self.bot.tools.path_loops+"ratios.json", self.data_ratio)
    
    def save_data_floppeurs(self):
        self.bot.tools.save_json(self.bot.tools.path_loops+"floppeurs.json", self.data_floppeurs)