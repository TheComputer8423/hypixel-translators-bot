import discord
from discord.ext import commands
from main import main_db

collection = main_db['context']


class crowdin_context(commands.Cog):
    name = "context"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def rip_you_lmao(self, ctx):
        await ctx.send("Have fun :kek:")


def setup(bot):
    bot.add_cog(crowdin_context(bot))
