import json
import discord

class Tools:
    def __init__(self):
        self.path_engine = "engine/"
        self.path_cogs = self.path_engine+"cogs/"
        self.path_loops = self.path_cogs+"loops/"
        self.path_maths = self.path_cogs+"maths/"
        self.path_polls = self.path_cogs+"polls/"
        self.path_pictures_polls = self.path_polls+"pictures/"
        self.path_prictures_maths = self.path_maths+"pictures/"
        self.list_alphabet_react = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "ℹ️", "🇯", "🇰", "🇱", "🇲", "🇳"]
        self.list_react_color = ["<:circle_0:1135250771777171588>", "<:circle_1:1135250877213573241>", "<:circle_2:1135250868409749575>", "<:circle_3:1135250866962698260>", "<:circle_4:1135250864592932995>", "<:circle_5:1135250863292682270>", "<:circle_6:1135250861715628124>", "<:circle_7:1135250859329077349>", "<:circle_8:1135250857814921236>", "<:circle_9:1135250854803415060>", "<:circle_10:1135250853327028374>", "<:circle_11:1135250851271802921>", "<:circle_12:1135250848432279753>", "<:circle_13:1135250846041522199>"]

    def load_json(self, path):
        data = None
        with open(path, "r") as f:
            data = json.load(f)
        return data
    
    def save_json(self, path, data):
        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4))
    
    def embed(self, title: str, color: discord.Colour, message: str, fields: list = None, image: discord.File = None, footer: str = None):
        embed = discord.Embed(title = title, description=message, color=color)
        if fields is not None:
            for field in fields:
                embed.add_field(name = field[0], value = field[1])
        if footer is not None:
            embed.set_footer(text=footer)
        return embed