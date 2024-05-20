import bcrypt
from aiogram.utils.text_decorations import markdown_decoration

from db import Book
from aiogram.utils.i18n import gettext as _


async def detail_book(book_id):
    book: Book = await Book.get(int(book_id))
    photo = book.photo
    nomi = _('Nomi')
    author = _('Avtor')
    pages = _('Bet')
    vol = _('Muqova')
    about = _('Malumot')
    price = _('Narxi')
    text = markdown_decoration.bold(f'''
{nomi}: {book.title}
{author}: {book.author}
{pages}: {book.pages}
{vol}: {book.cover}
{about}: {book.about}
{price}: {book.price}
    ''')
    return photo, text


def confirm_book(data):
    text = markdown_decoration.bold(f'''
Nomi: {data['title']}
Avtor: {data['author']}
Bet: {data['pages']}
Muqova: {data['cover']}
Malumot: {data['about']}
Narxi: {data['price']}
    ''')
    return text


def channel_detail(chat):
    text = markdown_decoration.bold(f'''
Chat
ID: {markdown_decoration.code(chat.id)}
Name: {chat.title}
Username: {chat.username}
Count users: {chat.get_member_count()}
    ''')
    return text

# import bcrypt
#
# key = bcrypt.hashpw(b'123', bcrypt.gensalt(12))
#
# print(key)