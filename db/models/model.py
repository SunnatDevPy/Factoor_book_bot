from select import select

from sqlalchemy import ForeignKey, BIGINT, Text, String, INT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import CreateModel, db


class User(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    orders: Mapped[list['Order']] = relationship('Order', back_populates='user')


class Categorie(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str]
    books: Mapped[list['Book']] = relationship('Book', back_populates='category')


class Book(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(Categorie.id, ondelete='CASCADE'))
    photo: Mapped[str] = mapped_column(Text())
    title: Mapped[str] = mapped_column(String())
    author: Mapped[str] = mapped_column(String())
    cover: Mapped[str] = mapped_column(String())
    about: Mapped[str] = mapped_column(String())
    pages: Mapped[int] = mapped_column(String())
    price: Mapped[int] = mapped_column(BIGINT())
    category: Mapped['Categorie'] = relationship('Categorie', back_populates='books')


class Order(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.id, ondelete='CASCADE'))
    book_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Book.id, ondelete='CASCADE'))
    count: Mapped[int] = mapped_column(INT)
    user: Mapped['User'] = relationship('User', back_populates='orders')

    # @classmethod
    # async def get_count_orders(cls, id_):
    #     query = select(func.count(Order)).where(Order.user_id == id_).group_by(Order)
    #     return (await db.execute(query)).scalar()


class History(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.id, ondelete='CASCADE'))
    text: Mapped[str] = mapped_column(Text())
    confirm: Mapped[bool] = mapped_column()



class Channels(CreateModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    url: Mapped[str] = mapped_column(String())
    title: Mapped[str] = mapped_column(String())
    private: Mapped[str] = mapped_column(String())
