import click

from app.ext.database import db
from app.ext.database.models import Saldos

@click.command('seed-saldos')
def seed_saldos():
    saldos = [
        {'ano': 2026, 'mes': 1, 'valor': 260.15, 'user_id': 1, 'banco_id': 1},
        {'ano': 2026, 'mes': 1, 'valor': 789.94, 'user_id': 2, 'banco_id': 2},
        {'ano': 2026, 'mes': 1, 'valor': 324.58, 'user_id': 1, 'banco_id': 3},
        {'ano': 2026, 'mes': 1, 'valor': 158.3, 'user_id': 2, 'banco_id': 4},
        {'ano': 2026, 'mes': 1, 'valor': 147.28, 'user_id': 1, 'banco_id': 4},
        {'ano': 2026, 'mes': 1, 'valor': 3000, 'user_id': 2, 'banco_id': 3},
        {'ano': 2026, 'mes': 1, 'valor': 136.89, 'user_id': 1, 'banco_id': 2},
        {'ano': 2026, 'mes': 1, 'valor': 144.15, 'user_id': 2, 'banco_id': 1},
    ]

    add = 0
    n_add = 0

    for s in saldos:
        if not db.session.query(Saldos).filter(Saldos.banco_id == s['banco_id'], Saldos.user_id == s['user_id'], Saldos.ano == s['ano'], Saldos.mes == s['mes']).first():
            saldo = Saldos(ano=s['ano'], mes=s['mes'], banco_id=s['banco_id'], valor=s['valor'], user_id=s['user_id'])
            db.session.add(saldo)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Saldos adicionados. {n_add} Saldos já existiam')