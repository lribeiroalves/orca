from flask import url_for
from flask_admin.contrib.sqla import ModelView


class MyModelView(ModelView):
    page_size = 50