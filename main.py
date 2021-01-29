from discord import ActivityType, AllowedMentions
from bot.Logger import Logger
from discord.ext import commands
import logging
import discord
import config


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s - %(name)s] %(message)s")
logging.getLogger("discord").setLevel(logging.WARNING)

bot = Logger(commands.when_mentioned_or(*config.prefixes),
                    case_insensitive=True,
                    owner_ids=config.owner_ids,
                    activity=discord.Activity(name=f"{config.prefixes[0]}help", type=ActivityType.listening),

                    # Regular client settings
                    max_messages=None,
                    intents=discord.Intents(messages=True, guilds=True, members=True),
                    allowed_mentions=AllowedMentions.none())

bot.run(config.token)
