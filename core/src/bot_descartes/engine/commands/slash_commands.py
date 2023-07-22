import discord
from discord.ext import commands
from discord import app_commands

class SlashCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="hi")
    async def hi_command(interaction:discord.Interaction):
        await interaction.response.send_message("Hi!")
