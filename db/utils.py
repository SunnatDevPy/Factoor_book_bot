from db import Book, History
from aiogram.utils.i18n import gettext as _

def count_orders(data):
    count = 0
    if data:
        for order in data:
            count += 1
    return count if count != 0 else None


async def settings_basket(orders, msg):
    list = []
    count = 1
    total = 0
    basket = _('🛒 Savat \n')
    tots = _('💸 Jami')
    for i in orders:
        book = await Book.get(int(i.book_id))
        text = f'{count}.📕 {book.title}\n{i.count} x {book.price} = {int(i.count) * int(book.price)} som\n'
        total += int(i.count) * int(book.price)
        count += 1
        list.append(text)
    else:
        s = basket + '\n'.join(list) + f'\n💸 {tots}: {total} som' + f'\n@{msg.from_user.username}'
        return s, total


async def settings_history(id_):
    history = await History.get_history(int(id_))
    number = _('Buyurtma raqami')
    data = _('Buyurtma qilingan sana')
    status = _('Buyurtma holati')
    book_name = _('Buyurtma holati')
    if history:
        list_ = []
        for i in history:
            text = f'''
🔢 {number}: {i.id}
📆 {data}: {i.created_at}
🟣 {status}: {_("🔄 kutish holatida") if i.confirm == True else _("❌ rad etilgan")}
📕 {book_name} 
{i.text}
            '''
            list_.append(text)
        return list_
    return