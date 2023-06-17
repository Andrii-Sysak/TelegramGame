import asyncio
import logging
# from asyncio import WindowsSelectorEventLoopPolicy

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from game.controllers.router import router
from game.db.session import eng
from game.utils.setup import init_db, configure_logging

TOKEN = '5929763272:AAGI1TK3zXbqzBy7yJ96hLO5Cih52YBJbiw'

logging.basicConfig(level=logging.INFO)

app = web.Application()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook('https://31.222.229.43:8443/webhook/main')


def main():
    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()
    # asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    dp.startup.register(on_startup)
    dp.include_router(router)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(
        app, path='/webhook/main'
    )
    setup_application(app, dp, bot=bot)


if __name__ == '__main__':
    configure_logging()
    main()
    asyncio.run(init_db())
    web.run_app(app, host='0.0.0.0', port=8080)
    asyncio.run(eng.dispose())
