from discord.ext.commands import Cog, Bot
from discord import app_commands, Interaction
from discord.ui import Modal, TextInput

class InputSystem(Modal):
    def __init__(self, inconnues: int, title: str):
        super().__init__(title=title)
        self.inconnues = inconnues

        for i in range(inconnues):
            self.add_item(TextInput(label=f'Équation {i+1}', custom_id=str(i)))

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message('ok')
        print(self.children)

class MathCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.variables = [*'xyzuv']
        self.letters = [*'abcdef']

    @app_commands.command(name='solve_system', description='Résout un système d\'équations')
    async def solve_system_command(self, interaction: Interaction, inconnues: int):
        if inconnues > 5:
            await interaction.response.send_message('Le bot ne peut pas résoudre un système de plus de 5 équations.')
            return
        elif inconnues < 1:
            await interaction.response.send_message('Le bot ne peut pas résoudre un système de moins de 1 équation.')
            return
        solution=f'{"+".join([self.letters[i]+self.variables[i] for i in range(inconnues)])}={self.letters[inconnues]}'
        await interaction.response.send_modal(InputSystem(inconnues, solution))

    @app_commands.command(name='eval', description='Évalue une expression')
    async def eval_comand(self, interaction: Interaction, expr: str):
        await interaction.response.send_message('WIP')

