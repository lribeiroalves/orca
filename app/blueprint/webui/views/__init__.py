from flask import render_template, abort, redirect, url_for, jsonify, flash, request, send_from_directory
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import extract
import random
import colorsys

from app.ext.database import db
from app.ext.database.models import *
from app import get_base_path
from .forms import FormFiltroTabelas, FormEntradaSaida, FormExcluir, FormSaldos

base_path = get_base_path()


def consulta_banco(user=1, ano=1, mes=1) -> dict:
    try:
        periodo = datetime(ano, mes, 1)
        prev_periodo = periodo - relativedelta(months=1)
        next_periodo = periodo + relativedelta(months=1)

        entradas = db.session.scalars(db.select(Entradas).where(Entradas.ano == int(ano), Entradas.mes == int(mes), Entradas.user_id == int(user))).all()
        saidas = db.session.scalars(db.select(Saidas).where(Saidas.ano == int(ano), Saidas.mes == int(mes), Saidas.user_id == int(user))).all()
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == int(ano), Saldos.mes == int(mes), Saldos.user_id == int(user))).all()

        ano_ant = prev_periodo.year
        mes_ant = prev_periodo.month

        saldos_ant = db.session.scalars(db.select(Saldos).where(Saldos.ano == ano_ant, Saldos.mes == mes_ant, Saldos.user_id == int(user))).all()

        user_nome = db.session.scalars(db.select(Users).where(Users.id == user)).first().nome

        total_entradas = 0
        total_saidas = 0
        total_saldos = 0
        total_saldos_ant = 0 

        if entradas:
            total_entradas = sum(entrada.valor for entrada in entradas)
        if saidas:
            total_saidas = sum(saida.valor for saida in saidas)
        if saldos:
            total_saldos = sum(saldo.valor for saldo in saldos)
        if saldos_ant:
            total_saldos_ant = sum(saldo.valor for saldo in saldos_ant)

        # graficos
        labels_resultado = ['Entradas', 'Saidas']
        values_resultado = [total_entradas, total_saidas]
        labels_saldos = ['Mês Passado', 'Mês Atual']
        values_saldos = [total_saldos_ant, total_saldos]
    except Exception as e:
        return None

    return {
        'entrada': entradas,
        'saida': saidas,
        'saldo': saldos,
        'total_entrada': total_entradas,
        'total_saida': total_saidas,
        'total_saldo': total_saldos,
        'total_saldo_ant': total_saldos_ant,
        'labels_resultado': labels_resultado,
        'values_resultado': values_resultado,
        'labels_saldo': labels_saldos,
        'values_saldo': values_saldos,
        'user': user_nome,
        'user_id': user,
        'prev_mes': prev_periodo.month,
        'prev_ano': prev_periodo.year,
        'next_mes': next_periodo.month,
        'next_ano': next_periodo.year
    }


def indexView():
    return render_template('index.html')


def tabelasView():
    form_filtros = FormFiltroTabelas()
    form_entrada_saida = FormEntradaSaida()
    form_excluir = FormExcluir()
    form_saldos = FormSaldos()

    req_ano = request.args.get('ano', type=int)
    req_mes = request.args.get('mes', type=int)
    req_user = request.args.get('user', type=int)
    req_aba = request.args.get('aba', type=str)
    if not req_aba:
        req_aba = 'entrada'

    if req_ano and req_mes and req_user:
        dados = consulta_banco(req_user, req_ano, req_mes)
    else:
        dados = consulta_banco(1, datetime.now().year, datetime.now().month)

    return render_template('tabelas.html', form_filtros=form_filtros, formInOut=form_entrada_saida, formExcluir=form_excluir, formSaldo=form_saldos, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], user=dados['user'], user_id=dados['user_id'], ano=req_ano if req_ano else str(datetime.now().year), mes=f'{req_mes:02}' if req_mes else f'{datetime.now().month:02}', total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], prev_mes=dados['prev_mes'], prev_ano=dados['prev_ano'], next_mes=dados['next_mes'], next_ano=dados['next_ano'], aba=req_aba)


def filtroTabelasForm():
    form = FormFiltroTabelas()
    ano, mes, user = (None, None, None)
    aba = 'entrada'

    if form.validate_on_submit():
        ano = int(form.ano.data)
        mes = int(form.mes.data)
        user = int(form.user.data)
        aba = form.tipo.data.split('-')
        
        if len(aba) > 1 and aba[1] == 'p':
            usuarios = db.session.scalars(db.select(Users.id)).all()
            index = usuarios.index(user)
            user = (index + 1) % len(usuarios) + 1

        aba = aba[0] if aba else 'entrada'

    else:
        flash(form.errors)

    return redirect(url_for('webui.tabelasView', ano=ano, mes=mes, user=user, aba=aba))


def entradaSaidaForm():
    form = FormEntradaSaida()
    aba = ''

    if form.validate_on_submit():
        if form.form_name.data == 'entrada':
            try:
                id = int(form.idInOut.data)
                if not id:
                    # NOVA ENTRADA
                    nova_entrada = Entradas(ano=int(form.ano.data), mes=int(form.mes.data), descricao=form.desc.data, valor=float(form.valor.data.replace(',', '.')), user_id=int(form.user.data))
                    db.session.add(nova_entrada)
                    flash('Entrada registrada com sucesso.')
                    aba = 'entrada'
                else:
                    # EDIÇÃO
                    entrada = db.session.scalars(db.select(Entradas).where(Entradas.id == id)).first()
                    if not entrada:
                        flash('Essa entrada não existe.')
                        return redirect(url_for('webui.indexView'))
                    else:
                        entrada.ano = int(form.ano.data)
                        entrada.mes = int(form.mes.data)
                        entrada.descricao = form.desc.data
                        entrada.valor = float(form.valor.data.replace(',', '.'))
                        entrada.user_id = int(form.user.data)
                        flash('Entrada editada com sucesso.')
                        aba = 'entrada'
                db.session.commit()
            except Exception as err:
                flash(f'Erro no Formulario: {err}')
                return redirect(url_for('webui.indexView'))
        elif form.form_name.data == 'saida':
            try:
                id = int(form.idInOut.data)
                if not id:
                    # NOVA SAIDA
                    nova_saida = Saidas(ano=int(form.ano.data), mes=int(form.mes.data), descricao=form.desc.data, valor=float(form.valor.data.replace(',', '.')), user_id=int(form.user.data))
                    db.session.add(nova_saida)
                    flash('Saida registrada com sucesso.')
                    aba = 'saida'
                else:
                    # EDIÇÃO
                    saida = db.session.scalars(db.select(Saidas).where(Saidas.id == id)).first()
                    if not saida:
                        flash('Essa saída não existe.')
                        return redirect(url_for('webui.indexView'))
                    else:
                        saida.ano = int(form.ano.data)
                        saida.mes = int(form.mes.data)
                        saida.descricao = form.desc.data
                        saida.valor = float(form.valor.data.replace(',', '.'))
                        saida.user_id = int(form.user.data)
                        flash('Saida editada com sucesso.')
                        aba = 'saida'
                db.session.commit()
            except Exception as err:
                flash(f'Erro no Formulario: {err}')
                return redirect(url_for('webui.indexView'))
        else:
            flash('Erro no Formulario')
            return redirect(url_for('webui.indexView'))
    else:
        flash(form.errors)
        return redirect(url_for('webui.indexView'))

    return redirect(url_for('webui.tabelasView', ano=int(form.ano.data), mes=int(form.mes.data), user=int(form.user.data), aba=aba))


def excluirForm():
    form = FormExcluir()
    aba = ''

    try:
        match form.tipoExcluir.data:
            case 'entrada':
                entrada = db.session.scalars(db.select(Entradas).where(Entradas.id == int(form.idExcluir.data))).first()
                db.session.delete(entrada)
                aba = 'entrada'
                flash('Entrada apagada com sucesso.')
            case 'saida':
                saida = db.session.scalars(db.select(Saidas).where(Saidas.id == int(form.idExcluir.data))).first()
                db.session.delete(saida)
                aba = 'saida'
                flash('Saida apagada com sucesso.')
            case 'saldo':
                saldo = db.session.scalars(db.select(Saldos).where(Saldos.id == int(form.idExcluir.data))).first()
                db.session.delete(saldo)
                aba = 'saldo'
                flash('Saldo apagado com sucesso.')
            case 'compra':
                pass
            case _:
                raise Exception('Houve um Erro de Tipo.')

        db.session.commit()

    except Exception as Err:
        flash(f'Erro: {Err}')
        return redirect(url_for('webui.indexView'))

    return redirect(url_for('webui.tabelasView', ano=int(form.anoExcluir.data), mes=int(form.mesExcluir.data), user=int(form.userExcluir.data), aba=aba))


def saldosForm():
    form = FormSaldos()
    aba='saldo'

    try:
        if form.validate_on_submit():
            id = abs(int(form.idSaldo.data))
            ano = int(form.anoSaldo.data)
            mes = int(form.mesSaldo.data)
            user = int(form.userSaldo.data)
            banco = int(form.bancoSaldo.data)
            valor = float(form.valorSaldo.data.replace(',', '.'))
            if not id:
                # NOVO SALDO
                novo_saldo = Saldos()
                novo_saldo.ano = ano
                novo_saldo.mes = mes
                novo_saldo.valor = valor
                novo_saldo.user_id = user
                novo_saldo.banco_id = banco

                db.session.add(novo_saldo)
                flash('Novo Saldo Registrado com Sucesso.')
            else:
                # EDIÇÃO DE SALDO
                saldo = db.session.scalars(db.select(Saldos).where(Saldos.id == id)).first()
                if saldo:
                    saldo.ano = ano
                    saldo.mes = mes
                    saldo.valor = valor
                    saldo.user_id = user
                    saldo.banco_id = banco

                    flash('Saldo Editado com suceso.')
                else:
                    raise Exception('Saldo não encontrado.')

            db.session.commit()
        else:
            raise Exception('Formulário não validado!')
    except Exception as Err:
        flash(f'ERRO: {Err}')
        return redirect(url_for('webui.indexView'))

    return redirect(url_for('webui.tabelasView', ano=int(form.anoSaldo.data), mes=int(form.mesSaldo.data), user=int(form.userSaldo.data), aba=aba))


def faturasView():
    return render_template('faturas.html')


def gerar_cores_aleatorias(n):
    if not n:
        return []

    cores = []

    matiz_inicial = random.random()

    salto = 1.0 / n

    for i in range(n):
        matiz = (matiz_inicial + i*salto) % 1.0
        saturacao = 0.8
        brilho = 0.9

        r_float, g_float, b_float = colorsys.hsv_to_rgb(matiz, saturacao, brilho)
        r = int(r_float * 255)
        g = int(g_float * 255)
        b = int(b_float * 255)

        luminosidade = (r * 299 + g * 587 + b * 114) / 1000

        cor_formatada = f'rgb({r}, {g}, {b})'
        cor_texto = "black" if luminosidade > 128 else "white"

        cores.append([cor_formatada, cor_texto])

    random.shuffle(cores)
    return cores



def faturasRequest():
    ano = request.args.get('ano')
    mes = request.args.get('mes')
    tipo = request.args.get('tipo')

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    if not ano or not mes:
        abort(400)
    else:
        try:
            ano = int(ano)
            mes= int(mes)
        except:
            abort(400)

    resposta = {}

    faturas = db.session.scalars(db.select(Faturas)).all()

    if faturas:
        resposta['anos'] = list(set([f.ano for f in faturas]))
        resposta['meses'] = list(set([meses[f.mes - 1] for f in faturas if f.ano == ano]))

        if tipo == 'mes':
            compras = db.session.scalars(db.select(Compras).join(Compras.fatura).where(Faturas.ano == ano, Faturas.mes == mes)).all()
            quantidade_usuarios = len(list(set([c.user_id for c in compras])))

            lista_cores = gerar_cores_aleatorias(quantidade_usuarios)

            users = {}
            for c in compras:
                if c.user_id in users.keys():
                    next
                users[c.user_id] = [c.user.nome, lista_cores[c.user_id - 1][0], lista_cores[c.user_id - 1][1]]
            resposta['users'] = users
            resposta['total_fatura'] = sum([c.valor_parcela for c in compras])
            resposta['total_por_usuario'] = [sum([c.valor_parcela for c in compras if c.user_id == u]) for u in users]
            resposta['dados'] = [c.to_dict() for c in compras]

        elif tipo == 'ano':
            pass
        else:
            abort(400)
    else:
        abort(400)

    return jsonify(resposta)

def graficosView():
    return render_template('graficos.html')






# Rota para servir o Manifest na raiz do site
def serve_manifest():
    static_images_dir = os.path.join(base_path, 'static', 'images')
    return send_from_directory(static_images_dir, 'site.webmanifest', mimetype='application/manifest+json')

# Rota para servir o Service Worker na raiz do site (Obrigatório para o escopo do PWA)
def serve_sw():
    static_js_dir = os.path.join(base_path, 'static', 'js')
    return send_from_directory(static_js_dir, 'sw.js', mimetype='application/javascript')