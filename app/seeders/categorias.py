import click

from app.ext.database import db
from app.ext.database.models import Categorias

@click.command('seed-categorias')
def seed_categorias():
    categorias = [
        {'nome': 'transporte'},
        {'nome': 'saúde'},
        {'nome': 'familia'},
        {'nome': 'roupas'},
        {'nome': 'gata'},
        {'nome': 'casa'},
        {'nome': 'alimentação'},
        {'nome': 'diversão'},
        {'nome': 'estudos'},
        {'nome': 'viagem'},
        {'nome': 'cartão'},
        {'nome': 'beleza'},
        {'nome': 'outros'},
    ]

    add = 0
    n_add = 0

    for c in categorias:
        if not db.session.query(Categorias).filter(Categorias.nome == c['nome']).first():
            categoria = Categorias(nome=c['nome'])
            db.session.add(categoria)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Categorias adicionadas. {n_add} Categorias já existiam')