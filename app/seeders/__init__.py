from .users import seed_users
from .bancos import seed_bancos


def populate_db(app):
    with app.app_context():
        seed_users.callback()
        seed_bancos.callback()


def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users, seed_bancos]:
            app.cli.add_command(command)

    populate_db(app)

    