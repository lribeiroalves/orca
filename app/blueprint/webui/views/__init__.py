from flask import render_template, abort, redirect, url_for, jsonify, flash, request, send_from_directory
import os

from app.ext.database import db
from app.ext.database.models import *
from app import get_base_path
from .forms import FormFiltroTabelas

base_path = get_base_path()


def consulta_banco(user=1, ano=1, mes=1) -> dict:
    try:
        entradas = db.session.scalars(db.select(Entradas).where(Entradas.ano == int(ano), Entradas.mes == int(mes), Entradas.user_id == int(user))).all()
        saidas = db.session.scalars(db.select(Saidas).where(Saidas.ano == int(ano), Saidas.mes == int(mes), Saidas.user_id == int(user))).all()
        saldos = db.session.scalars(db.select(Saldos).where(Saldos.ano == int(ano), Saldos.mes == int(mes), Saldos.user_id == int(user))).all()

        ano_ant = int(ano)
        mes_ant = int(mes) - 1
        if not mes_ant:
            mes_ant = 12
            ano_ant -= 1

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
        'user': entradas[0].user.nome
    }


def indexView():
    return render_template('index.html')


def tabelasView():
    form_filtros = FormFiltroTabelas()

    req_ano = request.args.get('ano', type=int)
    req_mes = request.args.get('mes', type=int)
    req_user = request.args.get('user', type=int)

    if req_ano and req_mes and req_user:
        dados = consulta_banco(req_user, req_ano, req_mes)
    else:
        return render_template('tabelas.html', form=form_filtros)

    return render_template('tabelas.html', form=form_filtros, entradas=dados['entrada'], saidas=dados['saida'], saldos=dados['saldo'], user=dados['user'], ano=req_ano, mes=f'{req_mes:02}', total_entradas=dados['total_entrada'], total_saidas=dados['total_saida'], total_saldos=dados['total_saldo'])


def filtroTabelasView():
    form = FormFiltroTabelas()
    ano, mes, user = (None, None, None)

    if form.validate_on_submit():
        ano = int(form.ano.data)
        mes = int(form.mes.data)
        user = int(form.user.data)
    else:
        flash(form.errors)

    return redirect(url_for('webui.tabelasView', ano=ano, mes=mes, user=user))


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