import discord
from discord.ext import commands
from main import main_db
from random import randint
from config import staff_bot_channel_id
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
    async def add(self, ctx, quote_author: discord.Member, *, quote_content: str):
        target_channel = ctx.bot.get_channel(staff_bot_channel_id)
        if ctx.message.author.guild_permissions.view_audit_log:
            quote_stats = collection.find_one({"id": "eugene"})
            total_quotes = quote_stats['total_quotes']
            new_total_quotes = total_quotes + 1
            author_id = quote_author.id
            new_quote = {"id": new_total_quotes, "quote": quote_content, "author": f"<@!{author_id}>"}
            collection.insert_one(new_quote)
            collection.update_one({"id": "eugene"}, {"$set": {"total_quotes": new_total_quotes}})

            staff_embed = discord.Embed(title="Success! The following quote was added:", color=discord.Colour.from_rgb(33, 222, 112))
            staff_embed.set_author(name='Quote')
            staff_embed.add_field(value=quote_content, name="Quote:", inline=False)
            staff_embed.add_field(value=f'- <@!{author_id}>', name="Said By:", inline=False)
            staff_embed.add_field(value=new_total_quotes, name="Quote ID:", inline=False)
            staff_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=staff_embed)
        else:
            user_embed = discord.Embed(title="Quote", color=discord.Colour.from_rgb(33, 222, 112))
            user_embed.add_field(value=f'\n{quote_content}\n- {quote_author}', name='Your quote request has been submitted, thanks!')
            user_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=user_embed)

            target_embed = discord.Embed(title="A quote request has been submitted!", color=discord.Colour.from_rgb(33, 222, 112))
            target_embed.set_author(name='Quote')
            target_embed.add_field(value=f"{quote_content}\n- <@!{quote_author.id}>", name='Quote:')
            target_embed.add_field(value=f"`+quote add {quote_author.id} {quote_content}`", name='To add it', inline=False)
            target_embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await target_channel.send(embed=target_embed)


def setup(bot):
    bot.add_cog(quote(bot))
