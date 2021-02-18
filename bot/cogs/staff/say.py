import discord
from discord.ext import commands
from main import main_db
from config import helper_id
import time
collection = main_db['users']


class say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.group()
    async def say(self, ctx, channel: discord.TextChannel, *, echo_content):
        helper_role = ctx.guild.get_role(helper_id)
        if helper_role in ctx.author.roles:
            await channel.send(f"> {echo_content}")
            embed = discord.Embed(title='Say', color=discord.Colour.red())
            embed.add_field(value=f'<#{channel.id}>:\n{echo_content}', name='Success! Message sent.', inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=embed)
        elif ctx.message.author.guild_permissions.view_audit_log:
            await channel.send(echo_content)
            embed = discord.Embed(title='Say', color=discord.Colour.red())
            embed.add_field(value=f'<#{channel.id}>:\n{echo_content}', name='Success! Message sent.', inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Error',
                                  description='You do not have sufficient permissions!', color=discord.Colour.red())
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=embed)
            time.sleep(10)
            await discord.Message.delete(ctx.message)


def setup(bot):
    bot.add_cog(say(bot))
