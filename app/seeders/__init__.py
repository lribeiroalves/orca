from .users import seed_users
from .bancos import seed_bancos
from .entradas import seed_entradas
from .saidas import seed_saidas
from .saldos import seed_saldos
from .faturas import seed_faturas
from .compras import seed_compras


def populate_db(app):
    with app.app_context():
        seed_users.callback()
        seed_bancos.callback()


def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users, seed_bancos, seed_entradas, seed_saidas, seed_saldos, seed_faturas, seed_compras]:
            app.cli.add_command(command)

    populate_db(app)

    