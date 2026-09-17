from flask import Blueprint
from datetime import datetime
import os

from .views import *
from app import get_base_path

base_path = get_base_path()

bp = Blueprint('graficos', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'graficos', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'graficos', 'content', 'templates'), static_url_path='/graficos/static', url_prefix='/graficos')

bp.add_url_rule('/', view_func=index_test)


def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime
