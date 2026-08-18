import click

from app.ext.database import db
from app.ext.database.models import Entradas

@click.command('seed-entradas')
def seed_entradas():
    entradas = [
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 1', 'valor': 1500.12, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 2', 'valor': 300, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 3', 'valor': 78.78, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 4', 'valor': 230.59, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 5', 'valor': 1800, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 6', 'valor': 325.48, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 7', 'valor': 951.28, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 8', 'valor': 78, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 9', 'valor': 2532.14, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada teste 10', 'valor': 1896, 'user_id': 2},
    ]

    add = 0
    n_add = 0

    for e in entradas:
        if not db.session.query(Entradas).filter(Entradas.descricao == e['descricao'], Entradas.valor == e['valor'], Entradas.ano == e['ano'], Entradas.mes == e['mes']).first():
            entrada = Entradas(ano=e['ano'], mes=e['mes'], descricao=e['descricao'], valor=e['valor'], user_id=e['user_id'])
            db.session.add(entrada)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Entradas adicionadas. {n_add} Entradas já existiam')