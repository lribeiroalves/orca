import click

from app.ext.database import db
from app.ext.database.models import Saidas

@click.command('seed-saidas')
def seed_saidas():
    saidas = [
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 1', 'valor': 260.15, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 2', 'valor': 789.94, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 3', 'valor': 324.58, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 4', 'valor': 158.3, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 5', 'valor': 147.28, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 6', 'valor': 3000, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 7', 'valor': 136.89, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 8', 'valor': 144.15, 'user_id': 2},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 9', 'valor': 1850.12, 'user_id': 1},
        {'ano': 2026, 'mes': 1, 'descricao': 'entrada saida 10', 'valor': 12, 'user_id': 2},
    ]

    add = 0
    n_add = 0

    for s in saidas:
        if not db.session.query(Saidas).filter(Saidas.descricao == s['descricao'], Saidas.valor == s['valor'], Saidas.ano == s['ano'], Saidas.mes == s['mes']).first():
            saida = Saidas(ano=s['ano'], mes=s['mes'], descricao=s['descricao'], valor=s['valor'], user_id=s['user_id'])
            db.session.add(saida)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Saidas adicionadas. {n_add} Saidas já existiam')