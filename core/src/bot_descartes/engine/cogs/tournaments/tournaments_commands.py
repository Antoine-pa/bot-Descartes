import discord
from discord.ext import commands
from discord import app_commands
import random

class ButtonMenuTournament(discord.ui.View):
    def __init__(self, bot: commands.Bot, tournament, message: discord.Message, user: discord.User):
        self.bot = bot
        self.tournament = tournament
        self.message = message
        self.user = user
        self.players = [self.user]
        super().__init__(timeout=None)
    
    def create_content(self):
        content = f"TOURNOIS :\n- Nombre de participants : {self.tournament.data_tournament[str(self.message.id)]['players_number']}\n- Joueurs ({len(self.players)}):\n"
        for player in self.players:
            content += f" - {player}\n"
        return content
        
    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user not in self.players:
            self.players.append(interaction.user)
        if len(self.players) == self.tournament.data_tournament[str(self.message.id)]["players_number"]:
            await self.message.channel.send("okay stop")
            self.clear_items()
            print(self.players)
            random.shuffle(self.players)
            print(self.players)
            for player in self.players:
                self.tournament.data_tournament[str(self.message.id)]["players"].append(player.id)
            self.bot.tools.save_json(self.bot.tools.path_tournaments+"tournaments.json", self.tournament.data_tournament)
        await interaction.response.defer()
        await self.message.edit(content=self.create_content(), view=self)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.danger)
    async def leave_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user == self.user: #si le créateur quitte le tournois:
            await interaction.response.send_message("Voulez-vous supprimer le tournois ?") #faire une View de suppression7
            return
        if interaction.user in self.players:
            self.players.remove(interaction.user)
        await interaction.response.defer()
        await self.message.edit(content=self.create_content())

class SelectMenuTournament(discord.ui.Select):
    def __init__(self, bot: commands.Bot, tournament, user):
        self.bot = bot
        self.tournament = tournament
        self.user = user
        options = [
            discord.SelectOption(label="2", value=0, description="2 joueurs"),
            discord.SelectOption(label="4", value=1, description="4 joueurs"),
            discord.SelectOption(label="8", value=2, description="8 joueurs"),
            discord.SelectOption(label="16", value=3, description="16 joueurs"),
            discord.SelectOption(label="32", value=4, description="32 joueurs"),
            discord.SelectOption(label="64", value=5, description="64 joueurs")
        ]
        super().__init__(placeholder="Choisis le nombre de joueurs.", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        message = interaction.message
        self.tournament.data_tournament[str(message.id)]["players_number"] = 2**(int(interaction.data["values"][0])+1)
        self.bot.tools.save_json(self.bot.tools.path_tournaments+"tournaments.json", self.tournament.data_tournament)
        await interaction.response.defer()
        self.view.clear_items()
        await message.edit(
            content=f"TOURNOIS :\n- Nombre de participants : {self.tournament.data_tournament[str(message.id)]['players_number']}\n- Joueurs (1):\n    - {self.user}",
            view=ButtonMenuTournament(self.bot, self.tournament, message, self.user)
        )
        
class SelectMenuTournamentView(discord.ui.View):
    def __init__(self, bot: commands.Bot, tournament, message, user):
        super().__init__(timeout=120)
        self.bot = bot
        self.message = message
        self.tournament = tournament
        self.user = user
        self.add_item(SelectMenuTournament(bot, tournament, user))

    async def interaction_check(self, interaction: discord.Interaction):
        return interaction.user == self.user
    
    async def on_timeout(self):
        del self.tournament.data_tournament[str(self.message.id)]
        self.bot.tools.save_json(self.bot.tools.path_tournaments+"tournaments.json", self.tournament.data_tournament)
        await self.message.channel.send("tournois annulé", delete_after=10)
        await self.message.delete()
        del self


class TournamentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.data_tournament = self.bot.tools.load_json(self.bot.tools.path_tournaments+"tournaments.json")

    @app_commands.command(name="create_tournament", description="création d'un tournois")
    async def create_tournament_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Création de tournois...", delete_after=5)
        message: discord.Message = await interaction.channel.send("Préparation...")
        user = interaction.user
        self.data_tournament[str(message.id)] = {"players_number": None, "players" : []}
        self.bot.tools.save_json(self.bot.tools.path_tournaments+"tournaments.json", self.data_tournament)
        await message.edit(content = "TOURNOIS :", view=SelectMenuTournamentView(self.bot, self, message, user))
