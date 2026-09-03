from flask import Blueprint
from datetime import datetime
import os

from .views import *
from app import get_base_path

base_path = get_base_path()

bp = Blueprint('webui', __name__, static_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'static'), template_folder=os.path.join(base_path, 'app', 'blueprint', 'webui', 'content', 'templates'), static_url_path='/webui/static')

bp.add_url_rule('/', view_func=indexView)
bp.add_url_rule('/tabelas', view_func=tabelasView)
bp.add_url_rule('/filtro-tabelas', view_func=filtroTabelasForm, methods=['POST'])
bp.add_url_rule('/entrada-saida', view_func=entradaSaidaForm, methods=['POST'])
bp.add_url_rule('/excluir', view_func=excluirForm, methods=['POST'])
bp.add_url_rule('/saldos', view_func=saldosForm, methods=['POST'])
bp.add_url_rule('/faturas', view_func=faturasView)
bp.add_url_rule('/faturas-request', view_func=faturasRequest)
bp.add_url_rule('/compras-form', view_func=comprasForm, methods=['POST'])
bp.add_url_rule('/request-compras', view_func=requestCompras)
bp.add_url_rule('/excluir-compras', view_func=excluirCompras)
bp.add_url_rule('/graficos', view_func=graficosView)

bp.add_url_rule('/manifest.json', view_func=serve_manifest)
bp.add_url_rule('/sw.js', view_func=serve_sw)

def init_app(app):
    app.register_blueprint(bp)
    app.jinja_env.globals['datetime'] = datetime