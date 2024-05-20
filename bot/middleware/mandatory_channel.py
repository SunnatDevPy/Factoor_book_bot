from aiogram import BaseMiddleware, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.types import Message

from bot.buttuns.inline import make_channels
from db.models.model import Channels


class JoinChannelMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler,
            event: Message,
            data
    ):
        channels = await Channels.get_all()
        if event.callback_query and event.callback_query.data == 'confirm_channel' or event.message:
            if event.callback_query:
                user = event.callback_query.from_user
            else:
                user = event.message.from_user
            bot: Bot = data['bot']
            form_kb = []
            for channel in channels:
                member = await bot.get_chat_member(channel.id, user.id)
                if member.status == ChatMemberStatus.LEFT:
                    form_kb.append(channel)

            if form_kb:
                if event.callback_query:
                    print(123)
                    try:
                        await event.callback_query.message.edit_text('Barchasiga obuna boling',
                                                                     reply_markup=await make_channels(form_kb, bot))
                    except:
                        await event.callback_query.message.answer('Barchasiga obuna boling',
                                                                  reply_markup=await make_channels(form_kb, bot))

                else:
                    await event.message.answer('Kanallarga azo bolmagansiz',
                                               reply_markup=await make_channels(form_kb, bot))
                return

            return await handler(event, data)
