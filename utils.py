import json
from discord import Colour, File, Embed, Message
from discord.ext.commands import Bot

def read_json(path: str):
    with open(path, 'r') as f:
        return json.load(f)

def write_json(path: str, data):
    with open(path, 'w') as f:
        data=json.dumps(data, indent=4)
        f.write(data)

def build_embed(title: str,
                color: Colour,
                message: str,
                fields = None,
                image: File = None,
                footer: str = None) -> Embed:
    embed = Embed(title=title, description=message, color=color)
    if fields is not None:
        for field in fields:
            embed.add_field(name=field[0], value=field[1])
    if footer is not None:
        embed.set_footer(text=footer)
    return embed

async def fetch_message(self, bot: Bot, chan_id, msg_id) -> Message:
    return await bot.get_channel(chan_id).fetch_message(msg_id)
