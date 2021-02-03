from typing import *
import json


async def get_strings(ctx) -> Tuple[dict, dict]:
    author_lang = "en"  # todo: change to get from database
    with open(f"strings/{author_lang}/{repr(ctx.command)}", "r") as f:
        localstings = json.load(f)
    with open(f"strings/{author_lang}/global.json", "r") as f:
        globalstrings = json.load(f)


    return localstings, globalstrings
