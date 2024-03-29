import logging
from aiogram import Bot, Dispatcher, types
from aiohttp import web

import config
from bot import dp
from models import base


async def on_startup(web_app: web.Application):
    await dp.bot.delete_webhook()
    await dp.bot.set_webhook(config.WEBHOOK_URL)
    await base.on_startup(dp)


async def execute(req: web.Request) -> web.Response:
    updates = [types.Update(**(await req.json()))]
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    try:
        await dp.process_updates(updates)
    except Exception as e:
        logging.error(e)
    finally:
        return web.Response()


if __name__ == '__main__':
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(await base.on_shutdown(dp))
    app.add_routes([web.post('/', execute)])
    web.run_app(app, port=config.WEBAPP_PORT, host=config.WEBAPP_HOST)
