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

    anos_base = [s[0] for s in saldos]
    anos = []
    meses = []
    for ano in range(min(anos_base), max(anos_base)+1):
        anos += [ano] * 12
        meses += MESES.values()


    series = [{'label': u.capitalize(), 'valores': []} for u in users]
    for i in range(len(anos)):
        for u in users:
            saldo_encontrado = False
            for linha in saldos:
                if linha[0] == anos[i] and MESES[linha[1]] == meses[i] and linha[2].nome == u:
                    saldo_encontrado = True
                    valor = linha[3]
            if not saldo_encontrado:
                valor = 0
            for item in series:
                if u == item['label'].lower():
                    item['valores'].append(valor)
                    break

    resposta = {
        'status': 'ok',
        'anos': anos,
        'meses': meses,
        'series': series
    }

    return jsonify(resposta)