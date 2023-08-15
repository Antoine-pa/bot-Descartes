import json
from discord import Colour, File, Embed, Message
from discord.ext.commands import Bot
import time
import datetime

def read_json(path: str):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        write_json(path, {})
        return {}

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

async def fetch_message(bot: Bot, chan_id, msg_id) -> Message:
    return await bot.get_channel(chan_id).fetch_message(msg_id)

def date_to_timestamp(date: str) -> int:
    if date.count("/") != 2:
        return
    timestamp = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple()) + 68400 #19h
    return timestamp