from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.utils.i18n import I18n, gettext as _, lazy_gettext as __
from bot.buttuns.inline import basket_detail, inl_categories, inl_for_basket, confirm_basket_yes_no
from bot.buttuns.simple import get_contact, menu_button
from config import Config, conf
from db import Order, History
from db.utils import count_orders, settings_basket, settings_history
from state.states import ConfirmBasket

order_router = Router()


@order_router.callback_query(F.data.startswith('count_'))
async def count_book(call: CallbackQuery, state: FSMContext):
    orders = await Order.get_orders(call.from_user.id)
    book_id = await state.get_data()
    data = call.data.split('_')
    count = int(data[-1])
    if data[1] == 'minus':
        if count > 1:
            count -= 1
            await call.message.edit_reply_markup(call.inline_message_id, reply_markup=basket_detail(count=count))
        else:
            await call.answer(_('Eng kamida 1 ta kitob buyurtma qilishingiz mumkin!😁'), show_alert=True)
    elif data[1] == 'plus':
        count += 1
        await call.message.edit_reply_markup(call.inline_message_id, reply_markup=basket_detail(count=count))
    elif data[1] == 'add':
        await Order.create(user_id=call.from_user.id, book_id=int(book_id['book_id']), count=count)
        await state.clear()
        await call.message.answer(_('Savatga qoshildi'))
        await call.message.answer('Category', reply_markup=await inl_categories(basket=count_orders(orders)))
    elif data[1] == 'back':
        await call.message.delete()
        await call.message.answer(_('Category'), reply_markup=await inl_categories(basket=count_orders(orders)))
        await state.clear()


@order_router.callback_query(F.data == 'basket_check')
async def check_basket(call: CallbackQuery):
    orders = await Order.get_orders(call.from_user.id)
    text = await settings_basket(orders, call)
    await call.message.answer(text[0], reply_markup=await inl_for_basket())


@order_router.callback_query(F.data == 'basket_no')
@order_router.callback_query(F.data == 'clear_basket')
async def clear_basket(call: CallbackQuery):
    orders = await Order.get_orders(call.from_user.id)
    await Order.delete_orders(call.from_user.id)
    await call.answer(_('Tozalandi'), show_alert=True)
    await call.message.answer(_('Category'), reply_markup=await inl_categories(basket=count_orders(orders)))


@order_router.callback_query(F.data == 'confirm_orders')
async def confirm_orders(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.set_state(ConfirmBasket.phone_number)
    await call.message.answer(_('Telefon raqmni jonating (Pastgi tugmani bosing)'), reply_markup=get_contact())


@order_router.message(ConfirmBasket.phone_number)
async def confirm_orders(msg: Message, state: FSMContext, bot: Bot):
    orders = await Order.get_orders(msg.from_user.id)
    text = await settings_basket(orders, msg)
    if msg.contact:
        await state.update_data(phone_number=msg.contact.phone_number)
        await state.set_state(ConfirmBasket.confirm)
        await msg.answer(text[0], reply_markup=await confirm_basket_yes_no())
    else:
        await msg.answer(_('Pastgi tugmani bosmadiz'), reply_markup=get_contact())


@order_router.callback_query(F.data == 'basket_yes', ConfirmBasket.confirm)
async def basket_yes(call: CallbackQuery, bot: Bot, state: FSMContext):
    data = await state.get_data()
    orders = await Order.get_orders(call.from_user.id)
    text = await settings_basket(orders, call)
    await bot.send_message(chat_id=conf.bot.ADMIN, text=text[0] + f'\nContact: {data.get("phone_number")}',
                           parse_mode=ParseMode.MARKDOWN)
    await History.create(user_id=call.from_user.id, text=text[0], confirm=True)
    await Order.delete_orders(call.from_user.id)
    await call.message.answer(_('✅ Hurmatli mijoz! Buyurtmangiz uchun tashakkur.'))
    price = [LabeledPrice(label=text[0], amount=text[1] * 100)]
    await call.message.answer_invoice('Books', str(text[0]), f'History_id', Config.bot.PAYMENT, 'UZS', price)


@order_router.message(lambda message: message.successful_payment)
async def pyment_connect(message: Message, bot: Bot):
    if message.successful_payment:
        await History.update(1, confirm=True)
        await message.answer(_('Tolovingiz uchun rahmat'))
        await message.answer(_('Bosh Menyu'), reply_markup=menu_button())


@order_router.message(F.text == __('📃 Mening buyurtmalarim'))
async def my_history(message: Message):
    s = await settings_history(message.from_user.id)
    if s:
        for i in s:
            await message.answer(i)
    else:
        await message.answer(_('Hali beri buyurtma qilmadiz'))
