from flask import Blueprint
from datetime import datetime

from .views import *

bp = Blueprint('webui', __name__, static_folder='app/blueprint/main/content/static', template_folder='app/blueprint/main/content/templates', static_url_path='/main/static')

bp.add_url_rule('/', view_func=index)

def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime