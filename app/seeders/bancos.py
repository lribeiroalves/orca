import click
from app.ext.database import db
from app.ext.database.models import Bancos

@click.command('seed-bancos')
def seed_bancos():
    bancos = [
        {'nome': 'Nubank'},
        {'nome': 'Mercado Pago'},
        {'nome': 'Sofisa'},
        {'nome': 'Banco do Brasil'},
    ]

    add = 0
    n_add = 0

    for b in bancos:
        if not db.session.query(Bancos).filter_by(nome=b["nome"]).first():
            banco = Bancos(nome=b['nome'])
            db.session.add(banco)
            add += 1
        else:
            n_add += 1
    
    db.session.commit()
    if add:
        click.echo(f'{add} Bancos adicionados. {n_add} Bancos ja existiam')
    