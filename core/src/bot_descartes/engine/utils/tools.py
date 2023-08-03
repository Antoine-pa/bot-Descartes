import json
import discord
from discord.ext import commands

class Tools:
    def __init__(self):
        self.path_engine = "engine/"
        self.path_cogs = self.path_engine+"cogs/"
        self.path_loops = self.path_cogs+"loops/"
        self.path_maths = self.path_cogs+"maths/"
        self.path_polls = self.path_cogs+"polls/"
        self.path_tournaments = self.path_cogs+"tournaments/"
        self.path_pictures_polls = self.path_polls+"pictures/"
        self.path_prictures_maths = self.path_maths+"pictures/"
        self.list_react_color = ['<:number_0:1135985729504284712>', '<:number_1:1135985726392119388>', '<:number_2:1135985677104853032>', '<:number_3:1135985675016097842>', '<:number_4:1135985673367728219>', '<:number_5:1135985670188441663>', '<:number_6:1135985669253116035>', '<:number_7:1135985667499901018>', '<:number_8:1135985665251749898>', '<:number_9:1135985663444009011>', '<:number_10:1135985660994519132>', '<:number_11:1135985659602022450>', '<:number_12:1135985658264039545>', '<:number_13:1135985655940386866>']

    @staticmethod
    def load_json(path):
        data = None
        with open(path, "r") as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def save_json(path, data):
        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4))
    
    @staticmethod
    def embed(title: str, color: discord.Colour, message: str, fields: list = None, image: discord.File = None, footer: str = None):
        embed = discord.Embed(title = title, description=message, color=color)
        if fields is not None:
            for field in fields:
                embed.add_field(name = field[0], value = field[1])
        if footer is not None:
            embed.set_footer(text=footer)
        return embed
    
    async def get_message(self, bot: commands.Bot, channel_id: int, message_id: int) -> discord.Message:
        return await bot.get_channel(channel_id).fetch_message(message_id)