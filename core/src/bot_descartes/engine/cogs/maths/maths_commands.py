import discord
from discord.ext import commands
from discord import app_commands

class MathsCog(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="cercle_trigo", description="affiche le cercle trigonométrique")
    async def cercle_trigo_command(self, interaction: discord.Interaction):
        with open(self.bot.tools.path_prictures_maths+"cercle_trigo.jpg", "rb") as f:
            await interaction.response.send_message(content="Cercle Trigonométrique :", file=discord.File(f))