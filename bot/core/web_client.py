import json as json_parser
from enum import StrEnum
from time import time

import aiohttp
from better_proxy import Proxy

from bot.core.entities import AirDropTask, Boost, Upgrade, Profile, Task, DailyCombo, Config, AirDropTaskId
from bot.core.headers import create_headers
from bot.utils import logger
from bot.utils.client import Client


class Requests(StrEnum):
    CONFIG = "https://api.hamsterkombatgame.io/clicker/config"
    ME_TELEGRAM = "https://api.hamsterkombatgame.io/auth/me-telegram"
    TAP = "https://api.hamsterkombatgame.io/clicker/tap"
    BOOSTS_FOR_BUY = "https://api.hamsterkombatgame.io/clicker/boosts-for-buy"
    BUY_UPGRADE = "https://api.hamsterkombatgame.io/clicker/buy-upgrade"
    UPGRADES_FOR_BUY = "https://api.hamsterkombatgame.io/clicker/upgrades-for-buy"
    BUY_BOOST = "https://api.hamsterkombatgame.io/clicker/buy-boost"
    CHECK_TASK = "https://api.hamsterkombatgame.io/clicker/check-task"
    SELECT_EXCHANGE = "https://api.hamsterkombatgame.io/clicker/select-exchange"
    LIST_TASKS = "https://api.hamsterkombatgame.io/clicker/list-tasks"
    SYNC = "https://api.hamsterkombatgame.io/clicker/sync"
    CLAIM_DAILY_CIPHER = "https://api.hamsterkombatgame.io/clicker/claim-daily-cipher"
    CLAIM_DAILY_COMBO = "https://api.hamsterkombatgame.io/clicker/claim-daily-combo"
    REFERRAL_STAT = "https://api.hamsterkombatgame.io/clicker/referral-stat"
    LIST_AIRDROP_TASKS = "https://api.hamsterkombatgame.io/clicker/list-airdrop-tasks"
    CHECK_AIRDROP_TASK = "https://api.hamsterkombatgame.io/clicker/check-airdrop-task"


class WebClient:
    def __init__(self, http_client: aiohttp.ClientSession, client: Client, proxy: str | None):
        self.http_client = http_client
        self.session_name = client.name
        self.http_client.headers["Authorization"] = f"Bearer {client.token}"
        self.proxy = proxy

    async def check_proxy(self, proxy: Proxy) -> None:
        try:
            response = await self.http_client.get(url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
            ip = (await response.json()).get('origin')
            logger.info(f"{self.session_name} | Proxy IP: {ip}")
        except aiohttp.ClientConnectorError as error:
            logger.error(f"{self.session_name} | Proxy: {proxy} | Error: {error}")

    async def get_profile_data(self) -> Profile:
        response = await self.make_request(Requests.SYNC)
        profile_data = response.get('clickerUser') or response.get('found', {}).get('clickerUser', {})
        return Profile(data=profile_data)

    async def get_tasks(self) -> list[Task]:
        response = await self.make_request(Requests.LIST_TASKS)
        return list(map(lambda d: Task(data=d), response['tasks']))

    async def select_exchange(self, exchange_id: str) -> bool:
        await self.make_request(Requests.SELECT_EXCHANGE, json={'exchangeId': exchange_id})
        return True

    async def check_task(self, task_id: str) -> bool:
        response = await self.make_request(Requests.CHECK_TASK, json={'taskId': task_id})
        return response.get('task', {}).get('isCompleted', False)

    async def apply_boost(self, boost_id: str) -> Profile:
        response = await self.make_request(Requests.BUY_BOOST, json={'timestamp': time(), 'boostId': boost_id})
        profile_data = response.get('clickerUser') or response.get('found', {}).get('clickerUser', {})

        return Profile(data=profile_data)

    async def get_upgrades(self) -> tuple[list[Upgrade], DailyCombo]:
        response = await self.make_request(Requests.UPGRADES_FOR_BUY)
        return list(map(lambda x: Upgrade(data=x), response['upgradesForBuy'])), \
            DailyCombo(data=response.get('dailyCombo', {}))

    async def buy_upgrade(self, upgrade_id: str) -> tuple[Profile, list[Upgrade], DailyCombo]:
        response = await self.make_request(Requests.BUY_UPGRADE, json={'timestamp': time(), 'upgradeId': upgrade_id})
        if 'found' in response:
            response = response['found']
        profile_data = response.get('clickerUser')
        return Profile(data=profile_data), \
            list(map(lambda x: Upgrade(data=x), response.get('upgradesForBuy', []))), \
            DailyCombo(data=response.get('dailyCombo', {}))

    async def get_boosts(self) -> list[Boost]:
        response = await self.make_request(Requests.BOOSTS_FOR_BUY)
        return list(map(lambda x: Boost(data=x), response['boostsForBuy']))

    async def send_taps(self, available_energy: int, taps: int) -> Profile:
        response = await self.make_request(Requests.TAP,
                                           json={'availableTaps': available_energy, 'count': taps, 'timestamp': time()})
        profile_data = response.get('clickerUser') or response.get('found', {}).get('clickerUser', {})

        return Profile(data=profile_data)

    async def get_me_telegram(self) -> None:
        await self.make_request(Requests.ME_TELEGRAM)

    async def get_config(self) -> Config:
        response = await self.make_request(Requests.CONFIG)
        return Config(data=response)

    async def claim_daily_cipher(self, cipher: str) -> Profile:
        response = await self.make_request(Requests.CLAIM_DAILY_CIPHER, json={'cipher': cipher})
        if 'found' in response:
            response = response['found']
        return Profile(data=response.get('clickerUser'))

    async def claim_daily_combo(self) -> Profile:
        response = await self.make_request(Requests.CLAIM_DAILY_COMBO)
        if 'found' in response:
            response = response['found']
        return Profile(data=response.get('clickerUser'))

    async def get_referrals_count(self) -> int:
        response = await self.make_request(Requests.REFERRAL_STAT, json={'offset': 0})
        if 'found' in response:
            response = response['found']
        return response.get('count', 0)

    async def attach_wallet(self, wallet: str) -> bool:
        response = await self.make_request(Requests.CHECK_AIRDROP_TASK,
                                           json={'id': AirDropTaskId.CONNECT_TON_WALLET, 'walletAddress': wallet})
        return response.get('airdropTask', {}).get('isCompleted', False)

    async def get_airdrop_tasks(self) -> list[AirDropTask]:
        response = await self.make_request(Requests.LIST_AIRDROP_TASKS)
        return list(map(lambda d: AirDropTask(data=d), response['airdropTasks']))

    async def make_request(self, request: Requests, json: dict | None = None) -> dict:
        response = await self.http_client.post(url=request,
                                               headers=create_headers(json),
                                               json=json)
        response_text = await response.text()
        if response.status != 422:
            response.raise_for_status()

        return json_parser.loads(response_text)
