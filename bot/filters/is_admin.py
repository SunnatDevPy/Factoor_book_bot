from aiogram.filters import Filter, BaseFilter
from aiogram.types import Message
from db.models.model import User

from config import conf


# class IsAdmin(BaseFilter):
#     def __init__(self, user_ids: list):
#         self.user_ids = user_ids
#
#     async def __call__(self, message: Message) -> bool:
#         admin_ids_int = [int(id) for id in self.user_ids]
#         return int(message.from_user.id) in admin_ids_int

class IsAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == conf.bot.ADMIN