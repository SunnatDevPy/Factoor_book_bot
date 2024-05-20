from aiogram.fsm.state import StatesGroup, State


class UpdateState(StatesGroup):
    update = State()


class UpdateBook(StatesGroup):
    category_id = State()
    column = State()
    new = State()
    update = State()


class CategoryCrtState(StatesGroup):
    change = State()
    category = State()


class BookState(StatesGroup):
    photo = State()
    category_id = State()
    title = State()
    author = State()
    cover = State()
    page = State()
    district = State()
    price = State()
    confirm = State()


class AddChannelState(StatesGroup):
    chat_id = State()
    confirm = State()


class ForwardState(StatesGroup):
    chat_id = State()

class ConfirmBasket(StatesGroup):
    phone_number = State()
    confirm = State()