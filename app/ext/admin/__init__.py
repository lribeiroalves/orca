from flask_admin import Admin, AdminIndexView, expose
from flask_admin.theme import Bootstrap4Theme

from app.ext.database import db
from app.ext.database.models import *
from .views import MyModelView


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


minhas_views = [
    MyModelView(Users, db.session),
    MyModelView(Bancos, db.session),
    MyModelView(Faturas, db.session),
    MyModelView(Categorias, db.session),
    MyModelView(Entradas, db.session),
    MyModelView(Saidas, db.session),
    MyModelView(Saldos, db.session),
    MyModelView(Compras, db.session),
]


def init_app(app):
    admin = Admin(app, name=app.config('TITLE'), theme=Bootstrap4Theme(swatch='cerulean'), index_view=MyAdminIndexView())
    admin.add_views(*minhas_views)