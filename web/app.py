import os

import uvicorn
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy_file.storage import StorageManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from config import conf
from db import User, History, Categorie, database, Book, Order
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key='1234')
]

app = Starlette(middleware=middleware)

logo_url = 'https://telegra.ph/file/9835206f0bff053fb5a10.png'
admin = Admin(
    engine=database._engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider()
)


class ProductModelView(ModelView):
    exclude_fields_from_list = ('created_at', 'updated_at')
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


class UserModelView(ModelView):
    exclude_fields_from_edit = ('created_at', 'updated_at')


class CategoryModelView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


class OrdersModelView(ModelView):
    exclude_fields_from_create = ('created_at', 'updated_at')
    exclude_fields_from_edit = ('created_at', 'updated_at')


# class HistoryModelView(ModelView):
#     exclude_fields_from_create = ('created_at', 'updated_at')
#     exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(UserModelView(User))
admin.add_view(CategoryModelView(Categorie))
admin.add_view(ProductModelView(Book))
admin.add_view(ModelView(History))
admin.add_view(ModelView(Order))

# Mount admin to your app
admin.mount_to(app)

# Configure Storage
os.makedirs("./media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
