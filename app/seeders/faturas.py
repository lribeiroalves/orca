import click

from app.ext.database import db
from app.ext.database.models import Faturas

@click.command('seed-faturas')
def seed_faturas():
    faturas = [
        {'ano': 2026, 'mes': 1, 'status_paga': False}
    ]

    add = 0
    n_add = 0

    for f in faturas:
        if not db.session.query(Faturas).filter(Faturas.ano == f['ano'], Faturas.mes == f['mes'], Faturas.status_paga == f['status_paga']).first():
            fatura = Faturas(ano=f['ano'], mes=f['mes'], status_paga=f['status_paga'])
            db.session.add(fatura)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Faturas adicionadas. {n_add} Faturas já existiam')