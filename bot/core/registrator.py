import asyncio
import glob
import os
from urllib.parse import unquote

import requests
from pyrogram import Client as TgClient
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions.messages import RequestWebView

from bot.config import settings
from bot.utils import logger
from bot.utils.client import Client
from bot.utils.fingerprint import FINGERPRINT
from bot.exceptions import InvalidSession


async def register_client() -> None:
    client_name = input('\nEnter the client name (press Enter to exit): ')

    if not client_name:
        return None

    token = input('\nEnter the token (press Enter to exit): ')

    if not token:
        return None
    await add_client(client=Client(name=client_name, token=token))


async def add_client(client: Client) -> None:
    if os.path.isdir('clients') is False:
        os.mkdir('clients')

    f = open(f"clients/{client.name}.client", "a")
    f.write(client.token)
    f.close()

    logger.success(f'Client `{client.name}` added successfully')


async def migrate_old_clients() -> None:
    if os.path.isdir('sessions') is False:
        logger.error('No sessions folder found')
        return

    session_names = glob.glob('sessions/*.session')
    session_names = [os.path.splitext(os.path.basename(file))[0] for file in session_names]

    if len(session_names) == 0:
        logger.error('Sessions folder is empty')
        return

    clients_migrated = 0

    for session_name in session_names:
        try:
            tg_client = TgClient(
                name=session_name,
                api_id=settings.API_ID,
                api_hash=settings.API_HASH,
                workdir='sessions/'
            )

            access_token = await auth(tg_client=tg_client)

            await add_client(client=Client(name=session_name, token=access_token))
            clients_migrated += 1
        except Exception as error:
            logger.error(f"Unknown error while getting Access Token: {error}")

    if clients_migrated == 0:
        logger.info('No clients migrated')
    else:
        logger.success(f'{clients_migrated} clients migrated successfully')


async def register_client_by_tg_auth() -> None:
    if not settings.API_ID or not settings.API_HASH:
        logger.error('API_ID or API_HASH is not set in the .env file')
        return None

    client_name = input('\nEnter the client name (press Enter to exit): ')

    if not client_name:
        return None

    try:
        tg_client = TgClient(
            name=client_name,
            api_id=settings.API_ID,
            api_hash=settings.API_HASH
        )
        async with tg_client:
            await tg_client.get_me()

        access_token = await auth(tg_client=tg_client)
        await tg_client.disconnect()

        await add_client(client=Client(name=client_name, token=access_token))
    except Exception as error:
        logger.error(f"Unknown error while getting Access Token: {error}")


async def auth(tg_client: TgClient) -> str | None:
    tg_web_data = await get_tg_web_data(tg_client)

    response = requests.post(url='https://api.hamsterkombatgame.io/auth/auth-by-telegram-webapp',
                             json={"initDataRaw": tg_web_data, "fingerprint": FINGERPRINT})

    return response.json().get('authToken')


async def get_tg_web_data(tg_client: TgClient) -> str | None:
    try:
        if not tg_client.is_connected:
            try:
                await tg_client.connect()
            except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                raise InvalidSession("hamster_bot")

        dialogs = tg_client.get_dialogs()
        async for dialog in dialogs:
            if dialog.chat and dialog.chat.username and dialog.chat.username == 'hamster_kombat_bot':
                break

        while True:
            try:
                peer = await tg_client.resolve_peer('hamster_kombat_bot')
                break
            except FloodWait:
                return None

        web_view = await tg_client.invoke(RequestWebView(
            peer=peer,
            bot=peer,
            platform='android',
            from_bot_menu=False,
            url='https://hamsterkombatgame.io/'
        ))

        auth_url = web_view.url
        tg_web_data = unquote(
            string=unquote(
                string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

        if tg_client.is_connected:
            await tg_client.disconnect()

        return tg_web_data

    except InvalidSession as error:
        raise error

    except Exception as error:
        logger.error(f"Unknown error during Authorization: {error}")
        await asyncio.sleep(delay=3)
