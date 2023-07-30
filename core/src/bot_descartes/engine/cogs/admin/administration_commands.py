import discord
from discord.ext import commands
from discord import app_commands

class AdministrationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="clear", description="Commande pour clear les messages.")
    @commands.has_permissions(manage_messages=True)
    async def clear_command(self, interaction: discord.Interaction, number: int, member:discord.Member = None):
        number = min(number+1, 50)
        channel = interaction.channel
        await interaction.response.send_message("Purge en cours")
        if member is None:
            await channel.purge(limit=number)
        else:
            def check(m):
                return m.author == member
            await channel.purge(limit=number,check=check)
        resp = await channel.send("Salon purgé.")
        await resp.delete(delay=5)