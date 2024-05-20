from aiogram import Bot
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Categorie, Book
from aiogram.utils.i18n import I18n, gettext as _


def language_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='🇺🇿Uz', callback_data='lang_uz'),
              InlineKeyboardButton(text='🇬🇧Eng', callback_data='lang_en'),
              InlineKeyboardButton(text='🇰🇷Kr', callback_data='lang_kor')])
    ikb.adjust(2)
    return ikb.as_markup()


async def inl_for_basket():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=_('❌ Savatni tozalash'), callback_data='clear_basket'),
              InlineKeyboardButton(text=_('✅ Buyurtmani tasdiqlash'), callback_data='confirm_orders'),
              InlineKeyboardButton(text=_('🔙Back🔙'), callback_data=f'back_category')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()

def network():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='Telegram', url='https://t.me/SunnatPyDev'),
              InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/_sunnat_0515_/'),
              InlineKeyboardButton(text='Google', url=f'https://www.google.com/')])
    ikb.adjust(1, repeat=True)
    return ikb.as_markup()

async def inl_categories(basket=False):
    categories: list[Categorie] = await Categorie.get_all()
    ikb = InlineKeyboardBuilder()
    for i in categories:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'categories_user_{i.id}')])
        ikb.adjust(2, repeat=True)
    else:
        if basket:
            ikb.row(InlineKeyboardButton(text=_(f'🛒 Savat ') + f'({basket})', callback_data='basket_check'))
        ikb.row(InlineKeyboardButton(text=_('🔍Search ...'), switch_inline_query_current_chat=''))
    return ikb.as_markup()


async def confirm_basket_yes_no(basket=False):
    ikb = InlineKeyboardBuilder()
    ikb.add(InlineKeyboardButton(text=_('Buyurtma beraszmi?'), callback_data='None_None'),
            InlineKeyboardButton(text=_('✅Ha'), callback_data='basket_yes'),
            InlineKeyboardButton(text=_('❌ Yo\'q'), callback_data='basket_no'))
    ikb.adjust(1, 2)
    return ikb.as_markup()


async def inl_book_buttons(category_id, basket=False):
    books = await Book.get_books(category_id)
    ikb = InlineKeyboardBuilder()
    for i in books:
        ikb.add(*[InlineKeyboardButton(text=i.title, callback_data=f'book_{i.id}')])
        ikb.adjust(2, repeat=True)
    else:
        ikb.row(*[InlineKeyboardButton(text=_('🔙Back🔙'), callback_data=f'back_category')])
        if basket:
            ikb.row(InlineKeyboardButton(text=_(f'🛒 Savat') + f'({basket})', callback_data='basket_check'))
    return ikb.as_markup()


async def settings_category_inl():
    categories: list[Categorie] = await Categorie.get_all()
    ikb = InlineKeyboardBuilder()
    for i in categories:
        ikb.add(*[InlineKeyboardButton(text=str(i.id), callback_data=f'admin_category_{i.id}'),
                  InlineKeyboardButton(text=i.title, callback_data=f'admin_category_{i.id}'),
                  InlineKeyboardButton(text="❌", callback_data=f'admin_category_clear_{i.id}')])
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


async def settings_book_inl(category_id):
    books = await Book.get_books(int(category_id))
    ikb = InlineKeyboardBuilder()
    for i in books:
        ikb.add(*[InlineKeyboardButton(text=str(i.id), callback_data=f'admin_book_{i.id}'),
                  InlineKeyboardButton(text=i.title, callback_data=f'admin_book_{i.id}'),
                  InlineKeyboardButton(text="❌", callback_data=f'admin_book_clear_{i.id}')])
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


def basket_detail(count=1):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='➖', callback_data=f'count_minus_{count}'),
              InlineKeyboardButton(text=str(count), callback_data=f'count_{count}'),
              InlineKeyboardButton(text='➕', callback_data=f'count_plus_{count}'),
              InlineKeyboardButton(text=_('⬅️Ortga'), callback_data=f'count_back_{count}'),
              InlineKeyboardButton(text=_('🗑 Savatga qo\'shish'), callback_data=f'count_add_{count}')])
    ikb.adjust(3, 2)
    return ikb.as_markup()


def confirm_book_inl():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text='✅Tasdiqlash✅', callback_data=f'confirm_book'),
              InlineKeyboardButton(text='❌Cancel❌', callback_data=f'cancel_book')])
    ikb.adjust(2, repeat=True)
    return ikb.as_markup()


async def make_channels(channel_ids, bot: Bot):
    ikb = InlineKeyboardBuilder()
    for channel in channel_ids:
        data = await bot.create_chat_invite_link(chat_id=channel.id)
        ikb.row(InlineKeyboardButton(text=_(f'Kanal ') + f'{channel.title}', url=data.invite_link))
    ikb.row(InlineKeyboardButton(text=_('Tasdiqlash'), callback_data='confirm_channel'))
    return ikb.as_markup()


def confirm_channels(title, url):
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text=_("Kanal ") + f'{title}', url=f'https://t.me/{url}')])
    ikb.add(*[InlineKeyboardButton(text="✅", callback_data='confirm_add_channel'),
              InlineKeyboardButton(text="❌", callback_data='cancel_add_channel')])
    ikb.adjust(1, 2)
    return ikb.as_markup()


def book_update_settings():
    ikb = InlineKeyboardBuilder()
    ikb.add(*[InlineKeyboardButton(text="photo", callback_data='photo')])
    ikb.add(*[InlineKeyboardButton(text='title', callback_data='title'),
              InlineKeyboardButton(text="author", callback_data='author'),
              InlineKeyboardButton(text="cover", callback_data='cover'),
              InlineKeyboardButton(text="about", callback_data='about'),
              InlineKeyboardButton(text="pages", callback_data='pages'),
              InlineKeyboardButton(text="price", callback_data='price')
              ])
    ikb.adjust(3, repeat=True)
    return ikb.as_markup()


async def show_channels(channels, bot: Bot):
    ikb = InlineKeyboardBuilder()
    for i in channels:
        channel = channels[i]
        data = await bot.create_chat_invite_link(int(i))
        ikb.add(*[InlineKeyboardButton(text=channel['title'], callback_data='channel_name'),
                  InlineKeyboardButton(text=i, callback_data='channel_id'),
                  InlineKeyboardButton(text='O\'tish', url=data.invite_link),
                  InlineKeyboardButton(text='❌', callback_data=f'clear_channel_{i}')])
    ikb.adjust(4, repeat=True)
    return ikb.as_markup()
