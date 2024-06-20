# pylint: disable=W0718

import asyncio
import base64
import datetime
import traceback
import random
from random import randint
from time import time

import aiohttp
from aiohttp_proxy import ProxyConnector

from bot.config import settings
from bot.core.entities import Upgrade, Profile, Boost, Task, Config, DailyCombo, Sleep, SleepReason
from bot.core.web_client import WebClient
from bot.exceptions import InvalidSession
from bot.utils import logger
from bot.utils.client import Client
from .headers import headers


class Tapper:
    def __init__(self, web_client: WebClient) -> None:
        self.web_client = web_client
        self.session_name = web_client.session_name
        self.profile = Profile(data={})
        self.upgrades: list[Upgrade] = []
        self.boosts: list[Boost] = []
        self.tasks: list[Task] = []
        self.daily_combo: DailyCombo | None = None
        self.preferred_sleep: Sleep | None = None

    def update_preferred_sleep(self, delay: float, sleep_reason: SleepReason):
        if self.preferred_sleep is not None and delay >= self.preferred_sleep.delay:
            return
        self.preferred_sleep = Sleep(delay=delay, sleep_reason=sleep_reason, created_time=time())

    async def earn_money(self):
        profile = await self.web_client.get_profile_data()

        self.profile = profile

        if self.profile.exchange_id == "hamster":
            await self.web_client.select_exchange(exchange_id="bybit")
            status = await self.web_client.check_task(task_id="select_exchange")
            if status is True:
                logger.success(f"{self.session_name} | Successfully selected exchange <y>Bybit</y>")

        logger.info(f"{self.session_name} | Last passive earn: <g>+{self.profile.last_passive_earn}</g> | "
                    f"Earn every hour: <y>{self.profile.earn_per_hour}</y>")

    async def check_daily_cipher(self, config: Config):
        if config.daily_cipher.is_claimed:
            return

        decoded_cipher = base64.b64decode(f"{config.daily_cipher.cipher[:3]}{config.daily_cipher.cipher[4:]}").decode(
            "utf-8")
        self.profile = await self.web_client.claim_daily_cipher(cipher=decoded_cipher)
        logger.success(f"{self.session_name} | Successfully get cipher reward | "
                       f"Cipher: <m>{decoded_cipher}</m> | Reward coins: <g>+{config.daily_cipher.bonus_coins}</g>")
        await self.sleep(delay=5)

    async def check_daily_combo(self):
        if not self.daily_combo.is_claimed:
            reward_claimed = await self.try_claim_daily_combo()
            if reward_claimed:
                return False

            combo = await fetch_daily_combo()
            if len(combo) == 0:
                logger.info(f"{self.session_name} | Daily combo not published")
                return False
            combo_upgrades: list[Upgrade] = list(
                filter(lambda u: u.id in combo and u.id not in self.daily_combo.upgrade_ids, self.upgrades))

            for upgrade in combo_upgrades:
                if not upgrade.can_upgrade():
                    logger.info(f"{self.session_name} | Can't upgrade <e>{upgrade.name}</e> for daily combo. Skipped")
                    return False
            for upgrade in combo_upgrades:
                if upgrade.price > self.profile.get_spending_balance():
                    logger.info(f"{self.session_name} | Not enough money for upgrade <e>{upgrade.name}</e>")
                    delay=int((upgrade.price - self.profile.get_spending_balance()) / self.profile.earn_per_sec)
                    if delay > 10500:  
                        delay = random.randint(3120, 7200)
                    self.update_preferred_sleep(
                        delay=delay,
                        sleep_reason=SleepReason.WAIT_UPGRADE_MONEY
                    )
                    return True

                await self.do_upgrade(upgrade=upgrade)

            await self.try_claim_daily_combo()
        return False

    async def try_claim_daily_combo(self) -> bool:
        if len(self.daily_combo.upgrade_ids) != 3:
            return False
        self.profile = await self.web_client.claim_daily_combo()
        logger.success(f"{self.session_name} | Successfully get daily combo reward | "
                       f"Reward coins: <g>+{self.daily_combo.bonus_coins}</g>")
        await self.sleep(delay=5)
        return True

    async def make_upgrades(self):
        wait_for_combo_upgrades = await self.check_daily_combo()
        if wait_for_combo_upgrades:
            return

        while True:
            available_upgrades = filter(lambda u: u.can_upgrade(), self.upgrades)

            if not settings.WAIT_FOR_MOST_PROFIT_UPGRADES:
                available_upgrades = filter(
                    lambda u: self.profile.get_spending_balance() > u.price and u.cooldown_seconds == 0,
                    available_upgrades)

            available_upgrades = sorted(available_upgrades, key=lambda u: u.calculate_significance(self.profile),
                                        reverse=False)

            if len(available_upgrades) == 0:
                logger.info(f"{self.session_name} | No available upgrades")
                break

            most_profit_upgrade: Upgrade = available_upgrades[0]

            if most_profit_upgrade.price > self.profile.get_spending_balance():
                logger.info(f"{self.session_name} | Not enough money for upgrade <e>{most_profit_upgrade.name}</e>")
                delay = int((most_profit_upgrade.price - self.profile.get_spending_balance()) / self.profile.earn_per_sec)
                if delay > 10500:  
                    delay = random.randint(3120, 7200)  
                self.update_preferred_sleep(
                    delay=delay,
                    sleep_reason=SleepReason.WAIT_UPGRADE_MONEY
                )
                break

            if most_profit_upgrade.cooldown_seconds > 0:
                logger.info(
                    f"{self.session_name} | "
                    f"Upgrade <e>{most_profit_upgrade.name}</e> on cooldown for <y>{most_profit_upgrade.cooldown_seconds}s</y>")
                self.update_preferred_sleep(
                    delay=most_profit_upgrade.cooldown_seconds,
                    sleep_reason=SleepReason.WAIT_UPGRADE_COOLDOWN
                )
                break

            await self.do_upgrade(upgrade=most_profit_upgrade)

    async def do_upgrade(self, upgrade: Upgrade):
        sleep_time = randint(settings.SLEEP_INTERVAL_BEFORE_UPGRADE[0], settings.SLEEP_INTERVAL_BEFORE_UPGRADE[1])
        logger.info(f"{self.session_name} | Sleep {sleep_time}s before upgrade <e>{upgrade.name}</e>")
        await self.sleep(delay=sleep_time)

        self.profile, self.upgrades, self.daily_combo = await self.web_client.buy_upgrade(upgrade_id=upgrade.id)

        logger.success(
            f"{self.session_name} | "
            f"Successfully upgraded <e>{upgrade.name}</e> to <m>{upgrade.level}</m> lvl | "
            f"Earn every hour: <y>{self.profile.earn_per_hour}</y> (<g>+{upgrade.earn_per_hour}</g>)")

    async def apply_energy_boost(self) -> bool:
        energy_boost = next((boost for boost in self.boosts if boost.id == 'BoostFullAvailableTaps'), {})
        if energy_boost.cooldown_seconds != 0 or energy_boost.level > energy_boost.max_level:
            return False

        profile = await self.web_client.apply_boost(boost_id="BoostFullAvailableTaps")

        self.profile = profile
        logger.success(f"{self.session_name} | Successfully apply energy boost")
        return True

    async def make_taps(self) -> bool:
        available_taps = self.profile.get_available_taps()
        if available_taps < self.profile.earn_per_tap:
            logger.info(f"{self.session_name} | Not enough taps: {available_taps}/{self.profile.earn_per_tap}")
            return True

        max_taps = int(float(self.profile.max_energy) / self.profile.earn_per_tap)
        taps_to_start = max_taps * settings.MIN_TAPS_FOR_CLICKER_IN_PERCENT / 100
        if available_taps < taps_to_start:
            logger.info(f"{self.session_name} | Not enough taps for launch clicker: {available_taps}/{taps_to_start}")
            return True

        current_energy = min(self.profile.available_energy, self.profile.max_energy)
        random_simulated_taps_percent = randint(1, 4) / 100
        # add 1-4% taps like official app when you're clicking by yourself
        simulated_taps = available_taps + int(available_taps * random_simulated_taps_percent)

        # sleep before taps like you do it in real like 6 taps per second
        sleep_time = int(available_taps / 6)
        logger.info(f"{self.session_name} | Sleep {sleep_time}s before taps")
        await self.sleep(delay=sleep_time)

        profile = await self.web_client.send_taps(available_energy=current_energy, taps=simulated_taps)

        new_balance = int(profile.balance)
        calc_taps = new_balance - self.profile.balance

        self.profile = profile

        logger.success(f"{self.session_name} | Successful tapped <c>{simulated_taps}</c> times! | "
                       f"Balance: <c>{self.profile.balance}</c> (<g>+{calc_taps}</g>)")
        return True

    async def sleep(self, delay: int):
        await asyncio.sleep(delay=float(delay))
        self.profile.available_energy = min(self.profile.available_energy + self.profile.energy_recover_per_sec * delay,
                                            self.profile.max_energy)
        self.profile.balance += self.profile.earn_per_sec * delay

    async def run(self) -> None:
        while True:
            try:
                # Sequence of requests in the client
                #     - me-telegram
                #     - config
                #     - sync
                #     - upgrades-for-buy
                #     - boosts-for-buy
                #     - list-tasks
                await self.web_client.get_me_telegram()
                config = await self.web_client.get_config()
                await self.earn_money()
                self.upgrades, self.daily_combo = await self.web_client.get_upgrades()
                self.boosts = await self.web_client.get_boosts()
                self.tasks = await self.web_client.get_tasks()

                # DAILY CIPHER
                await self.check_daily_cipher(config=config)

                # TASKS COMPLETING
                for task in self.tasks:
                    if task.is_completed is False:
                        if task.id == "invite_friends":
                            continue
                        status = await self.web_client.check_task(task_id=task.id)
                        if status is False:
                            continue

                        self.profile.balance += task.reward_coins
                        if task.id == "streak_days":
                            logger.success(f"{self.session_name} | Successfully get daily reward | "
                                           f"Days: <m>{task.days}</m> | "
                                           f"Balance: <c>{self.profile.balance}</c> (<g>+{task.reward_coins}</g>)")
                        else:
                            logger.success(f"{self.session_name} | Successfully get reward for task <m>{task.id}</m> | "
                                           f"Balance: <c>{self.profile.balance}</c> (<g>+{task.reward_coins}</g>)")

                # TAPPING
                if settings.AUTO_CLICKER is True:
                    await self.make_taps()

                    # APPLY ENERGY BOOST
                    if settings.APPLY_DAILY_ENERGY is True and time() - self.profile.last_energy_boost_time >= 3600:
                        logger.info(f"{self.session_name} | Sleep 5s before checking energy boost")
                        await self.sleep(delay=5)
                        if await self.apply_energy_boost():
                            await self.make_taps()

                    self.update_preferred_sleep(
                        delay=(
                                          self.profile.max_energy - self.profile.available_energy) / self.profile.energy_recover_per_sec,
                        sleep_reason=SleepReason.WAIT_ENERGY_RECOVER
                    )

                # UPGRADES
                if settings.AUTO_UPGRADE is True:
                    await self.make_upgrades()

                # SLEEP
                if self.preferred_sleep is not None:
                    sleep_time = max(self.preferred_sleep.delay - (time() - self.preferred_sleep.created_time), 40)
                    if self.preferred_sleep.sleep_reason == SleepReason.WAIT_UPGRADE_MONEY:
                        logger.info(f"{self.session_name} | Sleep {sleep_time}s for earn money for upgrades")
                    elif self.preferred_sleep.sleep_reason == SleepReason.WAIT_UPGRADE_COOLDOWN:
                        logger.info(f"{self.session_name} | Sleep {sleep_time}s for waiting cooldown for upgrades")
                    elif self.preferred_sleep.sleep_reason == SleepReason.WAIT_ENERGY_RECOVER:
                        logger.info(f"{self.session_name} | Sleep {sleep_time}s for recover full energy")

                    self.preferred_sleep = None
                    await self.sleep(delay=sleep_time)
                else:
                    logger.info(f"{self.session_name} | Sleep 3600s before next iteration")
                    await self.sleep(delay=3600)

            except InvalidSession as error:
                raise error
            except aiohttp.ClientResponseError as error:
                logger.error(f"{self.session_name} | Client response error: {error}")
                logger.info(f"{self.session_name} | Sleep 3600s before next iteration because of error")
                await self.sleep(delay=3600)
            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                traceback.print_exc()
                await self.sleep(delay=3)


async def run_tapper(client: Client, proxy: str | None):
    try:
        proxy_conn = ProxyConnector().from_url(proxy) if proxy else None

        async with aiohttp.ClientSession(headers=headers, connector=proxy_conn) as http_client:
            web_client = WebClient(http_client=http_client, client=client, proxy=proxy)
            await Tapper(web_client=web_client).run()
    except InvalidSession:
        logger.error(f"{client.name} | Invalid Session")


DAILY_JSON_URL = "https://anisovaleksey.github.io/HamsterKombatBot/daily_combo.json"


async def fetch_daily_combo() -> list[str]:
    async with aiohttp.ClientSession() as http_client:
        response = await http_client.get(url=DAILY_JSON_URL)
        response_json = await response.json()
        combo = response_json.get('combo')
        start_combo_date = datetime.datetime \
            .strptime(response_json.get('date'), "%Y-%m-%d") \
            .replace(tzinfo=datetime.timezone.utc).replace(hour=12)
        end_combo_date = start_combo_date + datetime.timedelta(days=1)
        current_timestamp = time()

        if start_combo_date.timestamp() < current_timestamp < end_combo_date.timestamp():
            return combo
        return []
