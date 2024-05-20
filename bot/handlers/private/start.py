from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.utils.i18n import I18n , gettext as _, lazy_gettext as __

from bot.buttuns.inline import language_inl, network
from bot.filters import IsAdmin
from bot.buttuns.simple import menu_button
from config import BOT, conf
from db import User

start_router = Router()


@start_router.message(CommandStart())
async def command_start(message: Message):
    # if IsAdmin():
    if int(conf.bot.ADMIN) == message.from_user.id:
        await message.answer('Hello admin', reply_markup=menu_button(admin=True))
        await message.answer(_('Til tanlang'), reply_markup=language_inl())
    else:
        user_data = {'id': message.from_user.id , 'username': message.from_user.username, 'full_name': message.from_user.full_name}
        user = await User.get(message.from_user.id)
        if not user:
            await User.create(**user_data)
            await message.answer(_('Til tanlang'), reply_markup=language_inl())
            await message.answer(_(f'Hello, ') + f' {markdown.bold(message.from_user.full_name)}!',
                                 reply_markup=menu_button())

        else:
            await message.answer(_('Til tanlang'), reply_markup=language_inl())
            await message.answer(_(f'Hello, ') + f' {markdown.bold(message.from_user.full_name)}!',
                                 reply_markup=menu_button())
            await message.bot.send_message(BOT.ADMIN, f'Create new user @{markdown.bold(message.from_user.username)}!')




# @start_router.message(F.text == __('📞 Biz bilan bog\'lanish'))
# async def start(message:Message):
#     tomon = _('tomonidan tayyorlandi')
#     await message.answer(f'Telegram: @logo_generate\n\n📞 + 99893 105 05 15\n Bot Yoqubov Sunnatilloh (@SunantDevPy) {tomon}.')


@start_router.message(F.text == __('🔵 Biz ijtimoiy tarmoqlarda'))
async def start(message:Message):
    await message.answer(_('Biz ijtimoiy tarmoqlarda'), reply_markup=network())