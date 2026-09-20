from flask import abort, jsonify
from sqlalchemy import func

from app.ext.database import db
from app.ext.database.models import *

MESES = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro'
}


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

    users = list(set([s[2].nome for s in saldos]))

    anos = [s[0] for s in saldos]
    anos = [v for i, v in enumerate(anos) if i % len(users) == 0]
    meses = [s[1] for s in saldos]
    meses = [MESES[v] for i, v in enumerate(meses) if i % len(users) == 0]

    series = [{'label': u.capitalize(), 'valores': []} for u in users]
    for linha in saldos:
        for item in series:
            if linha[2].nome == item['label'].lower():
                item['valores'].append(linha[3])
                continue

    resposta = {
        'status': 'ok',
        'anos': anos,
        'meses': meses,
        'series': series
    }

    return jsonify(resposta)