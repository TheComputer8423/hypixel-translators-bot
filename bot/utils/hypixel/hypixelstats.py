from math import floor, sqrt
import datetime
import aiohttp

EXP_FIELD = 0
LVL_FIELD = 0
BASE = 10000
GROWTH = 2500
HALF_GROWTH = 0.5 * GROWTH
REVERSE_PQ_PREFIX = -(BASE - 0.5 * GROWTH) / GROWTH
REVERSE_CONST = REVERSE_PQ_PREFIX * REVERSE_PQ_PREFIX
GROWTH_DIVIDES_2 = 2 / GROWTH


async def player_data_request(uuid, hypixel_api_key):
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={uuid}") as res:
                player_data = await res.json()
        print("player data was found")
        return player_data
    except:
        print("player data was not found")
        return None


async def name_to_uuid(username):
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?") as res:
                res_json = await res.json()
        return res_json["id"]
    except:
        return None


def get_rank(player_data):
    if "prefix" in player_data["player"]:
        player_prefix = (player_data["player"]["prefix"])
        if player_prefix == "§d[PIG§b+++§d]":
            return "[PIG+++]"
        elif player_prefix == "§c[SLOTH]":
            return "[SLOTH]"
        elif player_prefix == "§c[OWNER]":
            return '[OWNER]'
    if "rank" in player_data["player"]:
        rank = player_data["player"]["rank"]
        if rank == 'ADMIN':
            return '[ADMIN]'
        elif rank == 'MODERATOR':
            return '[MOD]'
        elif rank == 'HELPER':
            return '[HELPER]'
        elif rank == 'YOUTUBER':
            return '[YOUTUBE]'
    if "newPackageRank" in player_data["player"]:
        rank = (player_data["player"]["newPackageRank"])
        if rank == 'MVP_PLUS':
            if "monthlyPackageRank" in player_data["player"]:
                mvp_plus_plus = (player_data["player"]["monthlyPackageRank"])
                if mvp_plus_plus == "NONE":
                    return '[MVP+]'
                else:
                    return "[MVP++]"
            else:
                return "[MVP+]"
        elif rank == 'MVP':
            return '[MVP]'
        elif rank == 'VIP_PLUS':
            return 'VIP+'
        elif rank == 'VIP':
            return '[VIP]'
    else:
        return ''


def get_language(player_data):
    try:
        last_language_request = player_data['player']['userLanguage']
        return last_language_request
    except:
        return 'ENGLISH'


def get_last_login(player_data):
    try:
        last_login_request = player_data['player']['lastLogin']
        last_login_unformatted = datetime.datetime.fromtimestamp(last_login_request / 1000.0)
        last_login_output = (last_login_unformatted.strftime('%d %B %Y %X'))
        return last_login_output
    except:
        return 'This user has disabled their last login through their API settings.'


def get_first_login(player_data):
    try:
        first_login_request = player_data['player']['firstLogin']
        first_login_unformatted = datetime.datetime.fromtimestamp(first_login_request / 1000.0)
        first_login_output = (first_login_unformatted.strftime('%d %B %Y %X'))
        return first_login_output
    except:
        return 'This user has disabled their first login through their API settings.'


def get_last_game(player_data):
    try:
        last_game_request = player_data['player']['mostRecentGameType']
        return last_game_request
    except:
        return "This user has either never played a game or disabled their last game through their API settings."


def get_achievements(player_data):
    try:
        unformatted_user_achievements = player_data['player']['achievementPoints']
        user_achievements = '{:,}'.format(unformatted_user_achievements)
        return user_achievements
    except:
        return 0


def getLevel(exp):
    return floor(1 + REVERSE_PQ_PREFIX + sqrt(REVERSE_CONST + GROWTH_DIVIDES_2 * exp))


def getTotalExpToLevel(level):
    lv = floor(level)
    x0 = getTotalExpToFullLevel(lv)
    if level == lv:
        return x0
    else:
        return (getTotalExpToFullLevel(lv + 1) - x0) * (level % 1) + x0


def getTotalExpToFullLevel(level):
    return (HALF_GROWTH * (level - 2) + BASE) * (level - 1)


def getPercentageToNextLevel(exp):
    lv = getLevel(exp)
    x0 = getTotalExpToLevel(lv)
    return (exp - x0) / (getTotalExpToLevel(lv + 1) - x0)


def getExactLevel(player_data):
    try:
        exp = player_data['player']['networkExp']
        unformatted_exp = getLevel(exp) + getPercentageToNextLevel(exp)
        formatted_exp = '{:,.2f}'.format(unformatted_exp)
        return formatted_exp
    except:
        return None
