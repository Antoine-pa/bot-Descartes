import discord
from discord.ext import commands
from discord import app_commands

class TrollCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="ratio")
    async def ratio_command(self, interaction: discord.Interaction):
        #await interaction.response.send_message("ratio")
        await interaction.response.send_message("humm")
