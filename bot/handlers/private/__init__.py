from aiogram import Router, F
from aiogram.enums import ChatType

from bot.handlers.private.start import start_router
from bot.handlers.private.categories_handler import categories_router
from bot.handlers.private.book_handler import book_router
from bot.handlers.private.order_count import order_router

private_handler_router = Router()

# private_handler_router.callback_query.filter(F.chat.type == ChatType.PRIVATE)
# private_handler_router.message.filter(F.chat.type == ChatType.PRIVATE)

private_handler_router.include_routers(
    start_router,
    categories_router,
    book_router,
    order_router
)
