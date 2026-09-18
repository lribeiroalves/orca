from flask import abort, jsonify
from sqlalchemy import func

from app.ext.database import db
from app.ext.database.models import *


def index_test():
    return 'hello world!'


def get_patrimonio():
    stmt = (
        db.select(
                Saldos.ano,
                Saldos.mes,
                Users,
                func.sum(Saldos.valor).label('Valor')
            )
            .join(Saldos.user)
            .group_by(Saldos.ano, Saldos.mes, Users)
    )
    saldos = db.session.execute(statement=stmt).all()

    anos = list(set([s[0] for s in saldos]))
    meses = list(set([s[1] for s in saldos]))
    users = list(set([s[2] for s in saldos]))
    print(anos)
    print(meses)
    print(users)

    return 'ok'