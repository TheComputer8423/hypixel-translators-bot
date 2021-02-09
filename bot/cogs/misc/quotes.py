import discord
from discord.ext import commands
from main import main_db
from random import randint
from config import mod_id, admin_id, staff_bot_channel_id
collection = main_db['quotes_test']


class quote(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, quote_id: int = None):
        if ctx.invoked_subcommand is None:
            if quote_id is None:
                quote_stats = collection.find_one({"id": "eugene"})
                total_quotes = quote_stats['total_quotes']
                random_quote = randint(1, total_quotes)
                quote = collection.find_one({"id": random_quote})
                quote_author = quote['author']
                embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
                embed.add_field(value=f'- {quote_author}', name=quote['quote'])
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
                await ctx.send(embed=embed)
            else:
                quote = collection.find_one({"id": quote_id})
                quote_author = quote['author']
                embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
                embed.add_field(value=f'- {quote_author}', name=quote['quote'])
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
                await ctx.send(embed=embed)

    @quote.command()
    async def add(self, ctx, quote_author, *, quote_content: str):
        mod_role = ctx.guild.get_role(mod_id)
        admin_role = ctx.guild.get_role(admin_id)
        quote_mods = [mod_role, admin_role]
        target_channel = ctx.bot.get_channel(staff_bot_channel_id)
        if quote_mods in ctx.author.roles:
            # need to insert it into the database/make success message
            print("Add stuff here later hoggy")
        else:
            user_embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
            user_embed.add_field(value=f'\n{quote_content}\n- {quote_author}', name='Your quote request has been submitted, thanks!')
            user_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=user_embed)

            # Change embed to actually work
            target_embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
            target_embed.add_field(value=f'- {quote_author}', name='hi')
            target_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await target_channel.send(embed=target_embed)


def setup(bot):
    bot.add_cog(quote(bot))
