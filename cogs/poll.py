import asyncio
from config import PATHS, REACT_COLORS
from discord import app_commands, Message, File, Interaction, Embed, Colour
from discord.ext.commands import Cog, Bot
from dotenv import load_dotenv
from PIL import Image, ImageDraw
from os import getenv
from utils import read_json, write_json, build_embed

load_dotenv()

class PollCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
        self.pictures = PATHS['pictures']
        self.path_polls = f'{PATHS["storage"]}/{getenv("POLLS_STORAGE")}'
        self.data_polls = read_json(self.path_polls)

    def create_poll(self, guild, channel, ident: int, choices):
        self.data_polls[ident] = {'guild': guild,
                                       'channel': channel,
                                       'choices': {choice: 0 for choice in choices}}
        write_json(self.path_polls, self.data_polls)
        self.generate_diagram(ident, choices)

    def add_to_choice(msg: Message, idx: int, val: int):
        self.data_polls[msg.id]['choices'][idx] += val
        
    async def update_poll(self, message: Message, idx: int, val: int, old: int = None):
        add_to_choice(message, idx, val)
        if old is not None and val > 0:
            add_to_choice(message, idx, -1)

        write_json(self.path_polls, self.data_polls)
        self.update_diagram(message.id)
        embed = message.embeds[0]
        
        file = File(f'{self.pictures}/polls_{message.id}.png', filename='image.png')
        embed.set_thumbnail(url=f'attachment://image.png')
        embed.description=self.create_content(self.data_polls[message.id]['choices'])

        await message.edit(content='', embed=embed, attachments=[file])

    def generate_diagram(self, ident: int, choices):
        im = Image.new('RGBA', (500, 400), (255, 255, 255, 255))
        im.save(f'{self.pictures}/polls_diagram_{ident}.png')

    def update_diagram(self, ident: int):
        colors = [(241, 196, 15, 255), (243, 156, 18, 255), (230, 126, 34, 255), (211, 84, 0, 255),
            (192, 57, 43, 255), (231, 76, 60, 255), (155, 89, 182, 255), (142, 68, 173, 255),
            (41, 128, 185, 255), (52, 152, 219, 255), (26, 188, 156, 255), (22, 160, 133, 255),
            (39, 174, 96, 255), (46, 204, 113, 255)]
        im = Image.new('RGBA', (500, 400), (255, 255, 255, 255))
        draw = ImageDraw.Draw(im)
        start = 0
        data = self.data_polls[ident]['choices']
        vote_count = sum([d for d in data.values()])

        if vote_count == 0:
            self.generate_diagram(ident, data)
            return

        for i, d in enumerate(data.values()):
            end = start + d / vote_count * 360
            draw.pieslice((100, 50, 400, 350), start=start, end=end, fill=colors[i], outline=(255, 255, 255), width=2)
            start = end

        im.save(f'{self.pictures}/polls_diagram_{ident}.png')

    def create_content(self, choices):
        content = ''
        for i, (k, v) in enumerate(choices.items()):
            content += f'{REACT_COLORS[i]} : **{k}** ({v} votes)\n'
        return content[:-1]

    @app_commands.command(name='sondage', description='Crée un sondage (16 choix maximum, séparés par des `|\')')
    async def sondage_command(
            self,
            interaction: Interaction,
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
    ):
        reacts = REACT_COLORS
        choices = [c for c in [choix_1, choix_2, choix_3, choix_4, choix_5, choix_6, choix_7,
                               choix_8, choix_9, choix_10, choix_11, choix_12, choix_13, choix_14] if c is not None]
        message = await interaction.channel.send('Préparation...')

        self.create_poll(message.guild.id, message.channel.id, message.id, choices)
        file = File(f'{self.pictures}/polls_diagram_{message.id}.png', filename='image.png')
        embed = build_embed(title=titre,
                            color=Colour.red(),
                            message=self.create_content(self.data_polls[message.id]['choices']),
                            footer=f'Auteur : {interaction.user.name}\nIdentifiant du sondage : {message.id}')
        embed.set_thumbnail(url=f'attachment://image.png')

        await interaction.response.send_message('Votre sondage sera prêt dans un instant...', delete_after=5)
        await message.edit(attachments=[file], embed=embed, content='')

        for i, _ in enumerate(choices):
            await message.add_reaction(reacts[i])
