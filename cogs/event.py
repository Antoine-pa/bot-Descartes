import time
from config import REACT_COLORS
from discord import Message, RawReactionActionEvent
from discord.ext.commands import Cog, Bot

class EventCog(Cog):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

        @Cog.listener()
        async def on_message(self, message: Message):
            if message.author.id == self.bot.user.id:
                return
            if 'ratio' in content.split():
                await cogs.loops.ratio.RatioCog(bot).create_ratio(message)

        @Cog.listener()
        async def on_message_delete(self, message: Message):
            # Voir si le message est un sondage ou un ratio pour le
            # supprimer.
            pass

        async def poll_updater(self, payload: RawReactionActionEvent, value: int):
            if payload.user_id == self.bot.user.id:
                return
            pollcog = cogs.poll.PollCog(self.bot)
            if str(payload.message_id) in pollcog.data_polls:
                mx = pollcog.data_polls[str(payload.message_id)]['choices']
                list_react_color = REACT_COLORS[:len(mx)]

                if str(payload.emoji) in list_react_color:
                    message = await fetch_message(self.bot,
                                                  payload.channel_id,
                                                  payload.message_id)
                    await pollcog.update_poll(message,
                                              list_react_color.index(str(payload.emoji)),
                                              value)

        @Cog.listener()
        async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
            await self.poll_updater(payload, 1)

        @Cog.listener()
        async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
            await self.poll_updater(payload, -1)
