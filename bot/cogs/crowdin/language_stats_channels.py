import discord
from discord.ext import commands, tasks
from bot.utils.crowdin.api import *
import asyncio
from config import langstats_channels, newstrings_channels


class hypixelstats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.hp_sba.start()
        self.bot_qp.start()

    @tasks.loop(minutes=20)
    async def hp_sba(self):
        hplangstats = await hypixel()
        sbalangstats = await sba()

    @tasks.loop(minutes=20)
    async def bot_qp(self):
        htblangstats = await htb()
        qplangstats = await quickplay()

    @hp_sba.before_loop
    async def hp_sba_before_start(self):
        await self.bot.wait_until_ready()

    @bot_qp.before_loop
    async def bot_qp_before_start(self):
        await asyncio.sleep(600)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(hypixelstats(bot))
