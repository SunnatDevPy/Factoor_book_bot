from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.buttuns.inline import confirm_book_inl, inl_categories, basket_detail, settings_book_inl, \
    settings_category_inl, book_update_settings
from bot.buttuns.simple import settings_book, menu_button
from bot.detail_text import confirm_book, detail_book
from bot.filters import IsAdmin
from db import Book
from state.states import BookState, UpdateBook
from aiogram.utils.i18n import I18n , lazy_gettext as __, gettext as _
book_router = Router()


@book_router.callback_query(F.data.startswith("book_"))
async def book_callback_query(call: CallbackQuery, state: FSMContext, bot:Bot):
    detail = call.data.split('_')
    await state.update_data(book_id=detail[-1])
    photo = await detail_book(detail[-1])
    await bot.send_photo( chat_id=call.from_user.id,photo=photo[0], caption=photo[1], reply_markup=basket_detail())


@book_router.message(F.text == 'Book', IsAdmin())
async def book_handler(message: Message):
    await message.answer('Settings book', reply_markup=settings_book())


@book_router.message(F.text == 'Add Book', IsAdmin())
async def book_handler(message: Message, state: FSMContext):
    await state.set_state(BookState.category_id)
    await message.answer('Qaysi categoryga qoshmoqchsz', reply_markup=await settings_category_inl())


@book_router.callback_query(F.data.startswith('admin_category'), BookState.category_id, IsAdmin())
async def admin_category_callback(call: CallbackQuery, state: FSMContext):
    data = call.data.split('_')[-1]
    await state.update_data(category_id=data)
    await state.set_state(BookState.photo)
    await call.message.answer('Rasm jonating')


@book_router.message(BookState.photo, IsAdmin())
async def category_photo(message: Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
        await state.set_state(BookState.title)
        await message.answer('Kitobni nomini kiriting')
    else:
        await message.answer('Kiritilgan malumot rasim emas')


@book_router.message(BookState.title)
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(BookState.author)
    await message.answer('Kitobni avtorini kiriting')


@book_router.message(BookState.author)
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(author=message.text)
    await state.set_state(BookState.cover)
    await message.answer('Kitobni muqova holatini kiriting')


@book_router.message(BookState.cover)
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(cover=message.text)
    await state.set_state(BookState.page)
    await message.answer('Kitobni necha betligini kiriting')


@book_router.message(BookState.page)
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(pages=message.text)
    await state.set_state(BookState.district)
    await message.answer('Kitobni qoshimcha malumotni kiriting')


@book_router.message(BookState.district, IsAdmin())
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    await state.set_state(BookState.price)
    await message.answer('Kitobni narxini kiriting')


@book_router.message(BookState.price, IsAdmin())
async def category_photo(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()
    await state.set_state(BookState.confirm)
    text = confirm_book(data)
    await message.answer_photo(data['photo'], caption=text, reply_markup=confirm_book_inl())


@book_router.callback_query(F.data.endswith('_book'), IsAdmin())
async def callback_query(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    if call.data == 'confirm_book':
        data = await state.get_data()
        text = confirm_book(data)
        query = await Book.create(
            **{'category_id': int(data['category_id']), "photo": data['photo'], 'title': data['title'],
               'author': data['author'], 'cover': data['cover'], 'pages': data['pages'],
               'about': data['about'], "price": int(data['price'])})
        await call.message.answer_photo(data['photo'], caption=text + '\n' + 'Qoshildi')
    elif call.data == 'cancel_book':
        await call.message.answer('Protsess toxtatildi')
    await state.clear()


@book_router.message(F.text == 'Update Book', IsAdmin())
async def update_book(message: Message, state: FSMContext):
    await state.set_state(UpdateBook.category_id)
    await message.answer('qaysi categorydagi bookni ozgartrmoqchsz', reply_markup=await settings_category_inl())


@book_router.callback_query(F.data.startswith('admin_category'), UpdateBook.category_id, IsAdmin())
async def book_callback_query(call: CallbackQuery, state: FSMContext):
    detail = call.data.split('_')
    await state.update_data(category_id=detail[-1])
    await state.set_state(UpdateBook.column)
    await call.message.answer('Ozgartrmoqchi bolgan bookni tanlang', reply_markup=await settings_book_inl(detail[-1]))


@book_router.callback_query(F.data.startswith('admin_book'), IsAdmin(), UpdateBook.column)
async def admin_category_callback(call: CallbackQuery, state: FSMContext):
    book = call.data.split('_')
    await state.update_data(book_id=book[-1])
    if book[2] == 'clear':
        await Book.delete(int(book[-1]))
        await call.message.answer('Book ochdi')
        await call.message.edit_text('Category ', reply_markup=await settings_category_inl())
        await state.clear()
    else:
        text = await detail_book(book[-1])
        await call.message.delete()
        await state.set_state(UpdateBook.new)
        await call.message.answer_photo(text[0], caption=text[1])
        await call.message.answer('Tanlang', reply_markup=book_update_settings())


@book_router.callback_query(UpdateBook.new, IsAdmin())
async def new_callback(call: CallbackQuery, state: FSMContext):
    table = call.data
    await state.update_data(table_name=table)
    await call.message.answer('Yangi qiymat kiriting >> ')


@book_router.message(UpdateBook.new, IsAdmin())
async def new_callback(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = ''
    if message.photo:
        msg = message.photo[-1].file_id
    else:
        msg = message.text
    data = await state.get_data()
    await Book.update(int(data['book_id']), **{data['table_name']: msg})
    await message.answer('Book ozgardi', reply_markup=menu_button(admin=True))


@book_router.callback_query(F.data == 'back_category')
async def back_category(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(_('Books'), reply_markup=await inl_categories())
