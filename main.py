import asyncio
import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeChat
from aiogram import Dispatcher, Bot
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from bot import language_router
from bot.handlers import private_handler_router
from config import conf

from db import database


async def on_start(bot: Bot):
    await database.create_all()
    command_user = [BotCommand(command='start', description="Bo'tni ishga tushirish")]
    commands_admin = [
        BotCommand(command='start', description="Bo'tni ishga tushirish"),
        BotCommand(command='add', description="Kanal qoshish"),
        BotCommand(command='channels', description="Kanallar royxati"),
        BotCommand(command='get_id', description="id qaytarish")
    ]
    s = BotCommandScopeChat(chat_id=conf.bot.ADMIN)
    # await bot.set_my_commands(commands=commands_admin, scope=s)
    await bot.set_my_commands(commands=command_user)
    text = '«Factor books» nashriyotiga tegishli  rasmiy sotuv boti'
    await bot.set_my_description(text, 'uz')


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    await bot.delete_my_commands()


async def main():
    dp = Dispatcher()
    i18n = I18n(path="locales", default_locale='uz')
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    # dp.update.outer_middleware(JoinChannelMiddleware())
    dp.include_routers(private_handler_router, language_router)
    dp.startup.register(on_start)
    dp.shutdown.register(on_shutdown)
    bot = Bot(token=conf.bot.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
