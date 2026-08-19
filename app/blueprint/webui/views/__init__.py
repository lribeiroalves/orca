from flask import render_template, abort, redirect, url_for, jsonify, flash, request, send_from_directory
import os

from app import get_base_path
from .forms import FormFiltroTabelas

base_path = get_base_path()


def indexView():
    return render_template('index.html')


def tabelasView():
    form = FormFiltroTabelas()

    return render_template('tabelas.html', form=form)


def filtroTabelasView():
    return redirect(url_for('webui.tabelasView'))


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