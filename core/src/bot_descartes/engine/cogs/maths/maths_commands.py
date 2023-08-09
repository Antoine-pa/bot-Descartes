import discord
from discord.ext import commands
from discord import app_commands

class InputSystem(discord.ui.Modal):
    def __init__(self, inconnues: int, title:str):
        super().__init__(title=title)
        self.inconnues = inconnues
        for i in range(1, inconnues+1):
            self.add_item(discord.ui.TextInput(label=f"équation {i}", custom_id=str(i)))

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("ok")
        print(self.children)

class MathsCog(commands.Cog):
    def __init__(self, bot: commands.bot):
        super().__init__()
        self.bot = bot
        self.variables = ("x", "y", "z", "u", "v")
        self.letters = ("a", "b", "c", "d", "e", "f")
    
    @app_commands.command(name="cercle_trigo", description="affiche le cercle trigonométrique")
    async def cercle_trigo_command(self, interaction: discord.Interaction):
        with open(self.bot.tools.path_prictures_maths+"cercle_trigo.jpg", "rb") as f:
            await interaction.response.send_message(content="Cercle Trigonométrique :", file=discord.File(f))
    
    @app_commands.command(name="solve_system", description="Résout un système d'équation")
    async def solve_system_command(self, interaction: discord.Interaction, inconnues: int):
        if inconnues > 5:
            await interaction.response.send_message("nous ne pouvons pas faire plus qu'un système de 5 équations")
            return
        elif inconnues < 1:
            await interaction.response.send_message("impossible, le nombre d'inconnues doit être >= 1")
            return
        await interaction.response.send_modal(InputSystem(inconnues, f"{'+'.join([self.letters[i]+self.variables[i] for i in range(inconnues)])}={self.letters[inconnues]}"))

    @app_commands.command(name="eval", description="évalue une expression")
    async def eval_command(self, interaction: discord.Interaction, expression: str):
        await interaction.response.send_message("comming soon...")