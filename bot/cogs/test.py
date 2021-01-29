import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command()
    async def test(self, ctx):
        await ctx.send("Rodry is finally cool :)")


def setup(bot):
    bot.add_cog(test(bot))