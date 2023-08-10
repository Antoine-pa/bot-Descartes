import discord
import random
from config import PATHS
from discord import Message, User, ButtonStyle, Interaction, SelectOption, app_commands
from discord.ext.commands import Bot, Cog
from discord.ui import View, Button, Select
from dotenv import load_dotenv
from os import getenv
from utils import write_json, read_json

load_dotenv()

path_tournaments = f'{PATHS["storage"]}/{getenv("TOURNAMENTS_STORAGE")}'

class ButtonMenuTournament(View):
    def __init__(self, bot: Bot, tournament, message: Message, user: User):
        self.bot = bot
        self.tournament = tournament
        self.message = message
        self.user = user
        self.players = [self.user]
        super().__init__(timeout=None)

    def create_content(self):
        content = f'''
        TOURNOI :
        - Nombre de participants : {self.tournament.data_tournament[self.message.id]["player_count"]}
        - Joueurs ({len(self.players)}) :
        '''
        for player in self.players:
            content += f'- {player}\n'
        return content

    @discord.ui.button(label='Join', style=ButtonStyle.green)
    async def join_button(self, interaction: Interaction, button: Button):
        if interaction.user not in self.players:
            self.players.append(interaction.user)

        if len(self.players) == self.tournament.data_tournament[self.message.id]['player_count']:
            await self.message.channel.send('Fin des inscriptions.')
            self.clear_items()
            print(self.players)
            random.shuffle(self.plaers)
            print(self.players)
            for player in self.players:
                self.tournament.data_tournament[self.message.id]['players'].append(player.id)
            write_json(path_tournaments, self.tournament.data_tournament)

        await interaction.response.defer()
        await self.message.edit(content=self.create_content(), view=self)

    @discord.ui.button(label='Leave', style=ButtonStyle.danger)
    async def leave_buton(self, interaction: Interaction, button: Button):
        if interaction.user == self.user:
            await interaction.response.send_message('Voulez-vous supprimer le tournoi ?')
            return
        if interaction.user in self.players:
            self.players.remove(interaction.user)

        await interaction.response.defer()
        await self.message.edit(content=self.create_content())

class SelectMenuTournament(Select):
    def __init__(self, bot: Bot, tournament, user):
        self.bot = bot
        self.tournament = tournament
        self.user = user
        options = [
            SelectOption(label='2', value=0, description='2 joueurs'),
            SelectOption(label='4', value=1, description='4 joueurs'),
            SelectOption(label='8', value=2, description='8 joueurs'),
            SelectOption(label='16', value=3, description='16 joueurs'),
            SelectOption(label='32', value=4, description='32 joueurs'),
            SelectOption(label='64', value=5, description='64 joueurs')
        ]
        super().__init__(placeholder='Nombre de joueurs', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        message = interaction.message
        self.tournament.data_tournament[message.id]['player_count'] = 2**interaction.data['values'][0] + 1
        write_json(path_tournaments, self.tournament.data_tournament)

        await interaction.response.defer()

        self.view.clear_items()
        await message.edit(
            content=f'''
            TOURNOI :
            - Nombre de participants : {self.tournament.data_tournament[message.id]["player_count"]}
            - Joueurs (1) :
              - {self.user}''',
            view=ButtonMenuTournament(self.bot, self.tournament, message, self.user)
        )
        
class SelectMenuTournamentView(View):
    def __init__(self, bot: Bot, tournament, message, user):
        super().__init__(timeout=10)
        self.bot = bot
        self.message = message
        self.tournament = tournament
        self.user = user
        self.add_item(SelectMenuTournament(bot, tournament, user))

    async def interaction_check(self, interaction: Interaction):
        return interaction.user == self.user

    async def on_timeout(self):
        if self.children == []:
            return

        del self.tournament.data_tournament[self.message.id]

        write_json(path_tournaments, self.tournament.data_tournament)

        await self.message.channel.send('Tournois annulé.', delete_after=10)
        await self.message.delete()
        self.stop()

class TournamentCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.data_tournament = read_json(path_tournaments)

    @app_commands.command(name='create_tournament', description='Crée un tournoi')
    async def create_tournament_command(self, interaction: Interaction):
        await interaction.response.send_message('Création du tournoi...', delete_after=5)
        
        message = await interaction.channel.send('Préparation...')
        user = interaction.user
        self.data_tournament[message.id] = { 'player_count': None, 'players': [] }
        write_json(path_tournaments, self.data_tournament)

        await message.edit(content='TOURNOI', view=SelectMenuTournamentView(self.bot, self, message, user))
