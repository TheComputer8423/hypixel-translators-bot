import discord
from discord.ext import commands
from main import main_db
from random import randint
collection = main_db['quotes_test']


class quote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # cannot specify a quote yet
    @commands.group()
    async def quote(self, ctx):
        if ctx.invoked_subcommand is None:
            quote_stats = collection.find_one({"id": "eugene"})
            total_quotes = quote_stats['total_quotes']
            random_quote = randint(1, total_quotes)
            quote = collection.find_one({"id": random_quote})
            quote_author = quote['author']
            embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
            embed.add_field(value=f'- {quote_author}', name=quote['quote'])
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(quote(bot))
