import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw
import asyncio

class PollCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        super().__init__()
        self.bot = bot
        self.data_polls = self.bot.tools.load_json(self.bot.tools.path_polls+"polls.json")
    
    def create_poll(self, guild, channel, ident: int, choices: list):
        self.data_polls[str(ident)] = {"guild" : guild, "channel" : channel, "choices" : [[choice, 0] for choice in choices]}
        self.bot.tools.save_json(self.bot.tools.path_polls+"polls.json", self.data_polls)
        self.generate_diagram(ident, choices)
    
    async def update_poll(self, message: discord.Message, index_choice: int, value: int, old_choice: int= None):
        #changement des données :
        self.data_polls[str(message.id)]["choices"][index_choice][1] += value
        if old_choice is not None and value > 0:
            self.data_polls[str(message.id)]["choices"][old_choice][1] -= 1
        self.bot.tools.save_json(self.bot.tools.path_polls+"polls.json", self.data_polls)
        #update du diagramme :
        self.update_diagram(message.id)
        #edit du message :
        embed = message.embeds[0]
        file = discord.File(self.bot.tools.path_pictures_polls+str(message.id)+".png", filename="image.png")
        embed.set_thumbnail(url=f"attachment://image.png")
        embed.description=self.create_content(self.data_polls[str(message.id)]["choices"])
        await message.edit(content="", embed=embed, attachments=[file])
    
    def generate_diagram(self, ident: int, choices: list):
        im = Image.new('RGBA', (500, 400), (255, 255, 255, 255))
        im.save(self.bot.tools.path_pictures_polls+str(ident)+".png")
    
    def update_diagram(self, ident: int):
        colors = [(241, 196, 15, 255), (243, 156, 18, 255), (230, 126, 34, 255), (211, 84, 0, 255),
            (192, 57, 43, 255), (231, 76, 60, 255), (155, 89, 182, 255), (142, 68, 173, 255),
            (41, 128, 185, 255), (52, 152, 219, 255), (26, 188, 156, 255), (22, 160, 133, 255),
            (39, 174, 96, 255), (46, 204, 113, 255)]

        im = Image.new('RGBA', (500, 400), (255, 255, 255, 255))
        draw = ImageDraw.Draw(im)
        start = 0
        data = self.data_polls[str(ident)]["choices"]
        nb_vote = sum([d[1] for d in data])
        if nb_vote == 0:
            self.generate_diagram(ident, data)
            return
        for i in range(len(data)):
            end = start + data[i][1]/nb_vote*360
            draw.pieslice((100, 50, 400, 350), start=start, end=end, fill=colors[i], outline=(255, 255, 255), width=2)
            start = end
        im.save(self.bot.tools.path_pictures_polls+str(ident)+".png")
    

    def create_content(self, data_choices):
        content = ""
        for i in range(len(data_choices)):
            content += self.bot.tools.list_react_color[i] + " : **" + data_choices[i][0] + "** (" + str(data_choices[i][1]) + " votes)\n"
        return content[:-2]
            
    @app_commands.command(name="sondage", description="Création d'un sondage (16 choix max à séparer par des '|')")
    async def sondage_command(
        self, interaction: discord.Interaction,
        titre: str,
        choix_1: str,
        choix_2: str,
        choix_3: str = None,
        choix_4: str = None,
        choix_5: str = None,
        choix_6: str = None,
        choix_7: str = None,
        choix_8: str = None,
        choix_9: str = None,
        choix_10: str = None,
        choix_11: str = None,
        choix_12: str = None,
        choix_13: str = None,
        choix_14: str = None
    ) -> None:
        reacts = self.bot.tools.list_react_color
        choices = [c for c in [choix_1, choix_2, choix_3, choix_4, choix_5, choix_6, choix_7, choix_8, choix_9, choix_10, choix_11, choix_12, choix_13, choix_14] if c is not None]
        #message du sondage :
        message: discord.Message = await interaction.channel.send("Préparation...")

        self.create_poll(message.guild.id, message.channel.id, message.id, choices)
        file = discord.File(self.bot.tools.path_pictures_polls+str(message.id)+".png", filename="image.png")
        embed: discord.Embed = self.bot.tools.embed(title = titre, color = discord.Colour.red(), message = self.create_content(self.data_polls[str(message.id)]["choices"]), footer = f"auteur : {interaction.user.name}\nidentifiant du sondage : {message.id}")
        embed.set_thumbnail(url=f"attachment://image.png")
        #reponse à la commande :
        await interaction.response.send_message("Votre sondage est prêt dans une seconde...", delete_after=5)
        await message.edit(attachments=[file], embed=embed, content="")
        for i in range(len(choices)):
            await message.add_reaction(reacts[i])