from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import I18n, gettext as _

language_router = Router()

@language_router.callback_query(F.data.startswith('lang_'))
async def language_handler(call: CallbackQuery, state: FSMContext):
    lang_code = call.data.split('lang_')[-1]
    await state.update_data(locale=lang_code)
    await call.answer(_('Til tanlandi'), locale=lang_code, show_alert=True)
    await call.message.answer(_("Qayta /start bosing til ozgardi"))
