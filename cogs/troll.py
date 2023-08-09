from discord import Interaction, app_commands
from discord.ext.commands import Cog, Bot

import random

class TrollCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    @app_commands.command(name='ratio')
    async def ratio_command(self, interaction: Interaction):
        await interaction.response.send_message('humm')

    @app_commands.command(name='bite')
    async def bite_command(self, interaction: Interaction):
        await interaction.response.send_message(f'8{"="*random.randint(1,10)}D')
    
