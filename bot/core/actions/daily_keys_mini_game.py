from bot.core.entities import Config
from datetime import datetime
from random import randint
import base64


def get_keys_mini_game_cipher(config: Config, user_id: str) -> str:
    number = int(datetime.fromisoformat(config.daily_keys_mini_game.start_date.replace("Z", "+00:00")).timestamp())
    number_len = len(str(number))
    index = (number % (number_len - 2)) + 1
    res = ""

    for i in range(1, number_len + 1):
        if i == index:
            res += "0"
        else:
            res += str(randint(0, 9))

    return base64.b64encode(f"{res}|{user_id}".encode("utf-8")).decode("utf-8")
