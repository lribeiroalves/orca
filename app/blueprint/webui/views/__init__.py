from flask import render_template, abort, redirect, url_for, jsonify, flash, request, send_from_directory
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.ext.database import db
from app.ext.database.models import *
from app import get_base_path
from .forms import FormFiltroTabelas, FormEntradaSaida

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
        'user': entradas[0].user.nome if entradas else None,
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

    req_ano = request.args.get('ano', type=int)
    req_mes = request.args.get('mes', type=int)
    req_user = request.args.get('user', type=int)

    if req_ano and req_mes and req_user:
        dados = consulta_banco(req_user, req_ano, req_mes)
    else:
        dados = consulta_banco(1, datetime.now().year, datetime.now().month)

    return render_template('tabelas.html', form_filtros=form_filtros, formInOut=form_entrada_saida, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], user=dados['user'], user_id=dados['user_id'], ano=req_ano if req_ano else str(datetime.now().year), mes=f'{req_mes:02}' if req_mes else f'{datetime.now().month:02}', total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'], prev_mes=dados['prev_mes'], prev_ano=dados['prev_ano'], next_mes=dados['next_mes'], next_ano=dados['next_ano'])


def filtroTabelasForm():
    form = FormFiltroTabelas()
    ano, mes, user = (None, None, None)

    if form.validate_on_submit():
        ano = int(form.ano.data)
        mes = int(form.mes.data)
        user = int(form.user.data)
    else:
        flash(form.errors)

    return redirect(url_for('webui.tabelasView', ano=ano, mes=mes, user=user))


def entradaSaidaForm():
    form = FormEntradaSaida()

    if form.validate_on_submit():
        if form.form_name.data == 'entrada':
            try:
                id = int(form.idInOut.data)
                if not id:
                    # NOVA ENTRADA
                    nova_entrada = Entradas(ano=int(form.ano.data), mes=int(form.mes.data), descricao=form.desc.data, valor=float(form.valor.data.replace(',', '.')), user_id=int(form.user.data))
                    db.session.add(nova_entrada)
                    flash('Entrada registrada com sucesso.')
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

    return redirect(url_for('webui.tabelasView', ano=int(form.ano.data), mes=int(form.mes.data), user=int(form.user.data)))


def faturasView():
    return render_template('faturas.html')


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