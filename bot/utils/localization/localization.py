from typing import *
import json
from main import main_db


async def get_strings(ctx) -> Tuple[dict, dict]:
    collection = main_db['players']
    author_lang = collection.find_one({"id": str(ctx.author.id)})["lang"]

    with open(f"strings/{author_lang}/{ctx.command.name}.json", "r") as f:
        localstings = json.load(f)
    with open(f"strings/{author_lang}/global.json", "r") as f:
        globalstrings = json.load(f)


    return localstings, globalstrings
