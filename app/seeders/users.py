import click

from app.ext.database import db
from app.ext.database.models import Users


@click.command('seed-users')
def seed_users():
    usuarios = [
        {'nome': 'lucas'},
        {'nome': 'selma'},
    ]

    add = 0
    n_add = 0

    for u in usuarios:
        if not db.session.query(Users).filter_by(nome=u["nome"]).first():
            user = Users(nome=u['nome'])
            db.session.add(user)
            add += 1
        else:
            n_add += 1
    
    db.session.commit()
    if add:
        print(f'{add} Usuarios adicionados. {n_add} Usuarios ja existiam')
