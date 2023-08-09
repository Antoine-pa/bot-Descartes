import asyncio
import json
import time
from config import PATHS
from discord import Permissions, Colour
from discord.ext import tasks
from discord.ext.commands import Cog, Bot
from dotenv import load_dotenv
from os import getenv
from utils import read_json, write_json

load_dotenv()

class RatioCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.path_ratio = f'{PATHS["storage"]}/{getenv("RATIO_STORAGE")}'
        self.path_flops = f'{PATHS["storage"]}/{getenv("FLOPS_STORAGE")}'
        self.data_ratio = read_json(self.path_ratio)
        self.data_flops = read_json(self.path_flops)

    async def create_ratio(self, message):
        resp = await message.channel.send('Voulez-vous faire un ratio ?')

        await resp.add_reaction("✅")
        await resp.add_reaction("❌")

        try:
            check = lambda r, u: message.author.id == u.id and r.id == reaction.message.id \
                                                           and str(reaction.emoji) in ['✅', '❌']
            reaction, _ = await self.bot.wait_for('reaction_add',
                                                  timeout=10,
                                                  check=check)
        except:
            resp_ = await message.channel.send('Ratio annulé.')
            await resp.delete()
            await resp_.delete(delay=10)
            return

        if str(reaction) == '✅':
            logline = f'{message.author.id}{message.channel_id}'
            if logline in self.data_ratio:
                resp_ = await message.channel.send('Vous effectuez déjà un ratio dans ce salon.')
                await resp.delete()
                await resp_.delete(delay=10)
            await message.add_reaction('✅')
            await message.add_reaction('❌')
            self.data_ratio[logline] = {
                'start': time.time(),
                'channel': message.channel.id,
                'author': message.author.id,
                'message': message.id
            }
            self.save_data_ratio()
            await message.channel.send('Un ratio est lancé ! Il se finira dans 10 minutes.')
            
        await resp.delete()

    @tasks.loop(seconds=1)
    async def ratio_loop(self):
        delete_ratio = []

        for ratio, info in self.data_ratio.items():
            if time.time() - info['start'] > 10 * 60:
                delete_ratio.append(ratio)
                try:
                    channel = self.bot.get_channel(info['channel'])
                    user = self.bot.get_user(info['author'])
                    message = await channel.fetch_message(info['message'])

                    yes = 0
                    no  = 0

                    for react in messages.reactions:
                        if react.emoji == '✅':
                            yes += react.count - int(react.me)
                        elif react.emoji == '❌':
                            no += react.count - int(react.me)

                    if no >= yes:
                        await channel.send(f'Gros flop pour <@{user.id}>, tu gagnes le rôle de floppeur !')
                        guild = channel.guild
                        roles = await guild.fetch_roles()
                        role = None
                        role_flop = getenv('ROLE_FLOP')
                        for r in roles:
                            if r.name == role_flop and r.is_assignable():
                                role = r
                        if role is None:
                            role = await guild.create_role(name=role_flop,
                                                           permissions=Permissions(),
                                                           colour=Colour.blurple(),
                                                           hoist=True,
                                                           mentionable=True)
                        member = guild.get_member(user.id)
                        await member.add_roles(role)
                        key = f'{member.id}{guild.id}'

                        if key in self.data_flops:
                            self.data_flops[key]['start'] = time.time()
                        else:
                            self.data_flops[key] = {'start': time.time(),
                                                    'author': member.id,
                                                    'guild': guild.id,
                                                    'role': role.id
                                                    }
                        self.save_data_flops()
                    else:
                        await channel.send(f'Gros ratio de la part de <@{user.id}> !')
                except Exception as e:
                    print(e)
        for r in delete_ratio:
            del self.data_ratio[r]
        self.save_data_ratio()

    @tasks.loop(seconds=1)
    async def flops_loop(self):
        delete_flop = []
        
        for flop, info in self.data_flops.items():
            if time.time() - info['start'] >= 10 * 60:
                delete_flop.append(flop)
                try:
                    guild = self.bot.get_guild(info['guild'])
                    member = self.bot.get_member(info['author'])
                    role = guild.get_role(info['role'])

                    await member.remove_roles(role)
                except Exception as e:
                    print(e)
        for f in delete_flop:
            del self.data_flops[f]
        self.save_data_flops()

    @Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(1)
        self.ratio_loop.start()
        self.flops_loop.start()

    def save_data_ratio(self):
        write_json(self.path_ratio, self.data_ratio)

    def save_data_flops(self):
        write_json(self.path_flops, self.data_flops)
