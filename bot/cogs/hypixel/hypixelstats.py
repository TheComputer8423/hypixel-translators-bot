import discord
from discord.ext import commands
from config import hypixel_api_key
from bot.utils.hypixel.hypixelstats import *
from bot.utils.localization.localization import *

embed_description = "This information has been fetched from the Hypixel API. Some information may update slow due to \
how the API works."


class hypixelstats(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group(aliases=["hstats"], invoke_without_command=True)
    async def hypixelstats(self, ctx, username: str = None):
        strings, globalstrings = await get_strings(ctx)
        if username is None:

            embed = discord.Embed(title=globalstrings["error"],
                                  description=globalstrings['noUser'], color=discord.Colour.red())
            embed.add_field(value='`+hypixelstats <username>`', name=globalstrings['usage'], inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=strings['executedBy'].
                             replace("%%user%%", repr(ctx.author)) + " | " +
                             strings["madeBy"].replace("%%developer%%", "marzeq_#2137"))
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
            embed.set_author(name=strings["moduleName"])
            embed.set_thumbnail(url=f"https://mc-heads.net/body/{uuid}/left")
            embed.add_field(value=hypixel_level, name=strings["networkLevel"], inline=True)
            embed.add_field(value=achievement_points, name=strings["ap"], inline=True)
            embed.add_field(value=latest_language, name=strings["language"], inline=True)
            embed.add_field(value=first_login, name=strings["first_login"], inline=True)
            embed.add_field(value=last_login, name=strings["last_logout"], inline=True)
            embed.add_field(value=last_played, name='Last Played', inline=True)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed By {ctx.author}')
            await ctx.send(embed=embed)

    @hypixelstats.command()
    async def social(self, ctx, username: str = None):
        strings, globalstrings = await get_strings(ctx)
        if username is None:
            embed = discord.Embed(title=globalstrings["error"],
                                  description=globalstrings['noUser'], color=discord.Colour.red())
            embed.add_field(value='`+hypixelstats <username>`', name=globalstrings['usage'], inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=strings['executedBy'].
                             replace("%%user%%", repr(ctx.author)) + " | " +
                             strings["madeBy"].replace("%%developer%%", "marzeq_#2137"))
            await ctx.send(embed=embed)

        else:
            uuid = await name_to_uuid(username)
            player_data = await player_data_request(uuid, hypixel_api_key)
            rank = get_rank(player_data)
            twitter = user_twitter(player_data, username)
            youtube = user_youtube(player_data, username)
            instagram = user_instagram(player_data, username)
            twitch = user_twitch(player_data, username)
            disc = await user_discord(self, player_data)
            forums = user_forums(player_data, username)

            embed = discord.Embed(title=f'{rank} {username}',
                                  description=embed_description, color=discord.Colour.red())
            embed.set_author(name="Player Stats")
            embed.set_thumbnail(url=f"https://mc-heads.net/body/{uuid}/left")
            embed.add_field(value=twitter, name='Twitter', inline=True)
            embed.add_field(value=youtube, name='YouTube', inline=True)
            embed.add_field(value=instagram, name='Instagram', inline=True)
            embed.add_field(value=twitch, name='Twitch', inline=True)
            embed.add_field(value=disc, name='Discord', inline=True)
            embed.add_field(value=forums, name='Forums', inline=True)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed By {ctx.author}')
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(hypixelstats(bot))
