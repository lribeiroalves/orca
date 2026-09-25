from flask import abort, jsonify, request
from sqlalchemy import func
import random
import colorsys

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

def gerar_cores_aleatorias(usuarios):
    if not usuarios:
        return []

    n = len(usuarios)

    cores = []

    matiz_inicial = random.random()

    salto = 1.0 / n

    for i, id in enumerate(usuarios):
        matiz = (matiz_inicial + i*salto) % 1.0
        saturacao = 0.8
        brilho = 0.9

        r_float, g_float, b_float = colorsys.hsv_to_rgb(matiz, saturacao, brilho)
        r = int(r_float * 255)
        g = int(g_float * 255)
        b = int(b_float * 255)

        luminosidade = (r * 299 + g * 587 + b * 114) / 1000

        cor_formatada = f'rgb({r}, {g}, {b}, 0.7)'

        cores.append(cor_formatada)
        
    return cores


def index_test():
    return 'hello world!'


def get_patrimonio():
    try:
        r_ano = int(request.args['ano'])
        r_user = int(request.args['user'])
    except:
        r_ano, r_user = (0, 0, 0)

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
    filtros = []
    if r_ano:
        filtros.append(Saldos.ano == r_ano)
    if r_user:
        filtros.append(Saldos.user_id == r_user)

    if filtros:
        stmt = stmt.where(*filtros)

    saldos = db.session.execute(statement=stmt).all()
    if not saldos:
        return jsonify({
            'status': 'error'
        })

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

    cores = gerar_cores_aleatorias(users)

    resposta = {
        'status': 'ok',
        'anos': anos,
        'meses': meses,
        'series': series,
        'cores': cores
    }

    return jsonify(resposta)


def get_patrimonio_detalhado():
    """
        Criar grafico que mostra o saldo de conta que o usuario possui em cada mes
        O grafico vai mostrar um usuario de cada vez
        O grafico mostra um ano de cada vez ou detalha um mes de um ano especifico
        O grafico vai ter selecao de ano, de mes e de usuario
        requisicoes genericas retornam o ano mais recente, até o mes mais recente
        atualizar o dropdown de mes ao selecionar um ano com as opcoes disponiveis
    """

    try:
        ano = int(request.args['ano'])
        mes = int(request.args['mes'])
        user = int(request.args['user'])
        tipo = request.args['tipo']
        print(tipo, user, ano, mes)
    except:
        return jsonify({
            'status': 'error',
            'message': 'Argumentos inválidos.'
        })

    resposta = {
        'status': 'ok',
        'tipo': '',
        'message': '',
        'dados': {
            'users': None,
            'anos': None,
            'meses': None,
            'series': None,
            'cores': None,
        },
    }

    match tipo:
        case 'users':
            users = db.session.execute(db.select(Users.nome, Users.id)).all()
            if users:
                resposta['tipo'] = 'users'
                resposta['dados']['users'] = [{'nome': u[0].capitalize(), 'id': u[1]} for u in users]
            else:
                return jsonify(
                    {
                        'status': 'nok',
                        'message': 'Nenhum usuario encontrado.'
                    }
                )
        case 'anos':
            pass
        case 'meses':
            pass
        case 'grafico':
            pass
        case _:
            pass

    
    return jsonify(resposta)