import discord
from discord.ext import commands
from config import staff_bot_channel_id


class dm(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.bot.get_channel(staff_bot_channel_id)
        if not message.guild:
            if not message.author.bot:
                user_embed = discord.Embed(color=discord.Colour.from_rgb(33, 222, 112))
                user_embed.add_field(value=message.content, name="Sent message to staff", inline=False)
                user_embed.set_footer(text='Any messages sent here will be sent to staff.')
                await message.channel.send(embed=user_embed)
                staff_embed = discord.Embed(color=discord.Colour.from_rgb(40, 219, 222))
                staff_embed.add_field(value=message.content, name=f"Incoming message from {message.author}",
                                      inline=False)
                staff_embed.add_field(value=f'`+dm <{message.author.id}>`', name="To reply:", inline=False)
                await channel.send(embed=staff_embed)

    @commands.command()
    async def dm(self, ctx, target: discord.Member, *, dm_content: str):
        staff_role = ctx.guild.get_role(768435276191891456)
        if staff_role in ctx.author.roles:
            if target is None:
                embed = discord.Embed(color=discord.Colour.from_rgb(33, 222, 112))
                embed.add_field(value='You need to provide a user!', name="Error", inline=False)
                embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
                await ctx.send(embed=embed)
            else:
                if dm_content is None:
                    embed = discord.Embed(color=discord.Colour.from_rgb(33, 222, 112))
                    embed.add_field(value='You need to provide something to DM the user!', name="Error", inline=False)
                    embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(color=discord.Colour.from_rgb(40, 219, 222))
                    embed.add_field(value=dm_content, name="Received message from staff", inline=False)
                    embed.set_footer(text='Any messages sent here will be sent to staff.')
                    await target.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Colour.from_rgb(33, 222, 112))
            embed.add_field(value='You don\'t have permission to use this command!', name="Error", inline=False)
            embed.set_footer(icon_url=ctx.author.avatar_url, text=f'Executed by {ctx.author.name}')
            await ctx.send(embed=embed)









def setup(bot):
    bot.add_cog(dm(bot))
