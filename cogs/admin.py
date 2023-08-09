from dotenv import load_dotenv
from discord import app_commands, Interaction, Member
from discord.ext import commands
from discord.ext.commands import Cog, Bot
from os import getenv

load_dotenv()

def is_owner(ctx):
    return ctx.author.id in [int(i) for i in getenv('GUILD_OWNERS').split()]

class AdminCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name='clear', description='Clear les messages')
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, interaction: Interaction,
                            quantity: int, member: Member = None):
        quantity = min(quantity+1, 50)
        channel = interaction.channel
        await interaction.response.send_message('Purge en cours...')
        if member is None:
            await channel.purge(limit=quantity)
        else:
            await channel.purge(limit=quantity, check=lambda m: m.author == member)
        resp = await channel.send('Salon purgé.')
        await resp.delete(delay=5)

    def clean_code(self, code):
        code = code.strip('```')
        code = code.splitlines()

        if len(code) == 1 and '=' not in code[0]:
            one_line = True

        code = '\n'.join(code)
        
        return code, False if 'await' in code else one_line
