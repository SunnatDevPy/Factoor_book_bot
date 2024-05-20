from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import I18n, gettext as _


def menu_button(admin=False):
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text=_('📚 Kitoblar')),
             KeyboardButton(text=_('📃 Mening buyurtmalarim')),
             KeyboardButton(text=_('🔵 Biz ijtimoiy tarmoqlarda')),
             KeyboardButton(text=_('📞 Biz bilan bog\'lanish'))])
    if admin is True:
        kb.add(*[KeyboardButton(text='📊Statistika📊'),
                 KeyboardButton(text='⚙️Settings⚙️')])
    kb.adjust(2, repeat=True)
    return kb.as_markup(resize_keyboard=True)


def get_contact():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text=_('Contact jonatish'), request_contact=True)])
    return kb.as_markup(resize_keyboard=True)


def settings_menu():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='Category'),
             KeyboardButton(text='Book'),
             KeyboardButton(text='Back')])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def settings_category():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='Add Category'),
             KeyboardButton(text='Update Category'),
             KeyboardButton(text='Back')])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def settings_book():
    kb = ReplyKeyboardBuilder()
    kb.add(*[KeyboardButton(text='Add Book'),
             KeyboardButton(text='Update Book'),
             KeyboardButton(text='Back')])
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
