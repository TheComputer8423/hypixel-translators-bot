import discord
from discord.ext import commands
from config import hypixel_api_key
from bot.utils.hypixel.hypixelstats import *

embed_description = "This information has been fetched from the Hypixel API. Some information may update slow due to \
how the API works."


class hypixelstats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    # I'm setting it as a command group as I'm planning on adding subcategories (social, games, etc.)
    @commands.group()
    async def hypixelstats(self, ctx, username: str = None):
        if username is None:

            embed = discord.Embed(title=f'Error',
                                  description="**You haven't provided a username!**", color=discord.Colour.red())
            embed.add_field(value='`+hypixelstats <username>`', name='Expected Command Usage:', inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed By {ctx.author}')
            await ctx.send(embed=embed)

        else:

            uuid = await name_to_uuid(username)
            player_data = await player_data_request(uuid, hypixel_api_key)
            rank = get_rank(player_data)
            hypixel_level = getExactLevel(player_data)
            achievement_points = get_achievements(player_data)
            latest_language = get_language(player_data)
            first_login = get_first_login(player_data)
            last_login = get_last_login(player_data)
            last_played = get_last_game(player_data)

            embed = discord.Embed(title=f'{rank} {username}',
                                  description=embed_description, color=discord.Colour.red())
            embed.set_author(name="Player Stats")
            embed.set_thumbnail(url=f"https://mc-heads.net/body/{uuid}/left")
            embed.add_field(value=hypixel_level, name='Hypixel Level', inline=True)
            embed.add_field(value=achievement_points, name='Achievement Points', inline=True)
            embed.add_field(value=latest_language, name='Language', inline=True)
            embed.add_field(value=first_login, name='First Login', inline=True)
            embed.add_field(value=last_login, name='Last Login', inline=True)
            embed.add_field(value=last_played, name='Last Played', inline=True)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed By {ctx.author}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(hypixelstats(bot))
