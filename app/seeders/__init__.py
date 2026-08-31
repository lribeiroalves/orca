import click

from .users import seed_users
from .bancos import seed_bancos
from .entradas import seed_entradas
from .saidas import seed_saidas
from .saldos import seed_saldos
from .faturas import seed_faturas
from .categorias import seed_categorias
from .compras import seed_compras


@click.command('populate-development')
def populate_development():
    try:
        seed_users.callback()
        seed_bancos.callback()
        seed_categorias.callback()
        seed_faturas.callback()
        seed_entradas.callback()
        seed_saidas.callback()
        seed_saldos.callback()
        seed_compras.callback()
        click.echo('Banco dev populado com sucesso')
    except Exception as e:
        click.echo(e)

def init_app(app):
    if app.config['ENV'] == 'development':
        for command in [seed_users, seed_bancos, seed_entradas, seed_saidas, seed_saldos, seed_faturas, seed_compras, seed_categorias, populate_development]:
            app.cli.add_command(command)

    