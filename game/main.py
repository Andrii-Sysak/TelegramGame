import asyncio
import logging

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    setup_application,
)

from game.config import (
    Config,
    UpdateStrategy,
)
from game.controllers.router import router
from game.db.session import eng
from game.utils.setup import (
    init_db,
    configure_logging,
    init_config,
)

logging.basicConfig(level=logging.INFO)

app = web.Application()


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    if Config.c.updates_strategy is UpdateStrategy.webhook:
        await bot.set_webhook('https://31.222.229.43/webhook/main')


def main():
    init_config()
    session = AiohttpSession()
    bot = Bot(token=Config.c.token, session=session)
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_router(router)
    asyncio.run(init_db())
    if Config.c.updates_strategy is UpdateStrategy.webhook:
        SimpleRequestHandler(dispatcher=dp, bot=bot).register(
            app, path='/webhook/main'
        )
        setup_application(app, dp, bot=bot)
        web.run_app(app, host='0.0.0.0', port=8080)
    elif Config.c.updates_strategy is UpdateStrategy.polling:
        asyncio.run(dp.start_polling(bot))
    asyncio.run(eng.dispose())


if __name__ == '__main__':
    configure_logging()
    main()
