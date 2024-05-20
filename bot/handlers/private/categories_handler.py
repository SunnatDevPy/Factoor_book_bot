from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import I18n , lazy_gettext as __, gettext as _
from bot.buttuns.simple import settings_menu, menu_button, settings_category
from bot.filters.is_admin import IsAdmin
from bot.buttuns.inline import inl_categories, inl_book_buttons, settings_category_inl
from db import Categorie, Order
from db.utils import count_orders
from state.states import UpdateState, CategoryCrtState

categories_router = Router()


@categories_router.message(F.text == 'Back', IsAdmin())
async def settings(message: Message):
    await message.answer('Salom admin', reply_markup=menu_button(admin=True))


@categories_router.message(F.text == '⚙️Settings⚙️', IsAdmin())
async def settings(message: Message):
    await message.answer('Salom admin', reply_markup=settings_menu())


@categories_router.message(F.text == __('📚 Kitoblar'))
async def categories(message: Message):
    orders = await Order.get_orders(message.from_user.id)
    await message.answer('Categoriyalar',
                         reply_markup= await inl_categories(basket=count_orders(orders)))


@categories_router.callback_query(F.data.startswith('categories_'))
async def book_callback(call: CallbackQuery, state: FSMContext):
    orders = await Order.get_orders(call.from_user.id)
    detail = call.data.split('_')
    await state.update_data(category_id=detail[-1])
    await state.set_state(UpdateState.update)
    await call.message.edit_text(_('Books'), reply_markup=await inl_book_buttons(int(detail[-1]),
                                                                              basket=count_orders(orders)))


@categories_router.message(UpdateState.update)
async def category_update(message: Message, state: FSMContext):
    orders = await Order.get_orders(message.from_user.id)
    data = await state.get_data()
    await Categorie.update(int(data['category_id']), title=message.text)
    await message.answer(_('Category'),
                         reply_markup=await inl_categories(
                             basket=orders.count if orders else False))
    await state.clear()


@categories_router.message(F.text == __('Category'), IsAdmin())
async def category_delete(message: Message):
    await message.answer('Tanlang >> ', reply_markup=settings_category())



@categories_router.message(F.text == 'Add Category', IsAdmin())
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryCrtState.category)
    await message.answer('Category nomini kiriting >> ')


@categories_router.message(CategoryCrtState.category, IsAdmin())
async def category_delete(message: Message, state: FSMContext):
    orders = await Order.get_orders(message.from_user.id)
    await Categorie.create(title=message.text)
    await message.answer('Yangi Category qoshildi')
    await message.answer('Category',
                         reply_markup=await inl_categories(basket=count_orders(orders)))
    await state.clear()


@categories_router.message(F.text == 'Update Category', IsAdmin())
async def add_category(message: Message, state: FSMContext):
    await state.set_state(CategoryCrtState.change)
    await message.answer('Categoryni tanlang >> ', reply_markup=await settings_category_inl())


@categories_router.callback_query(F.data.startswith('admin_category'), IsAdmin(), CategoryCrtState.change)
async def admin_category_callback(call: CallbackQuery, state: FSMContext):
    category = call.data.split('_')
    await state.update_data(category_id=category[-1])
    if category[2] == 'clear':
        await Categorie.delete(int(category[-1]))
        await call.message.answer('Category ochdi')
        await call.message.edit_text('Category ', reply_markup=await settings_category_inl())
        await state.clear()
    else:
        await call.message.delete()
        await state.set_state(CategoryCrtState.category)
        await call.message.answer('Category namega kiriting >> ')


@categories_router.message(CategoryCrtState.category, IsAdmin())
async def admin_category_callback(message: Message, state: FSMContext):
    data = await state.get_data()
    await Categorie.update(int(data['category_id']), name=message.text)
    await message.answer('Category ozgardi', reply_markup=await settings_category_inl())
