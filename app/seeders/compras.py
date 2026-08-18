import click

from app.ext.database import db
from app.ext.database.models import Compras

@click.command('seed-compras')
def seed_compras():
    compras = [
        {'valor_total': 100, 'valor_parcela': 100, 'descricao': 'teste compra 1', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 200, 'valor_parcela': 200, 'descricao': 'teste compra 2', 'parcelas': 1, 'user_id': 2, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 300, 'valor_parcela': 300, 'descricao': 'teste compra 3', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 400, 'valor_parcela': 400, 'descricao': 'teste compra 4', 'parcelas': 1, 'user_id': 2, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 500, 'valor_parcela': 500, 'descricao': 'teste compra 5', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 6500, 'valor_parcela': 6500, 'descricao': 'teste compra 6', 'parcelas': 1, 'user_id': 2, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 70, 'valor_parcela': 70, 'descricao': 'teste compra 7', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 800, 'valor_parcela': 800, 'descricao': 'teste compra 8', 'parcelas': 1, 'user_id': 2, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 900, 'valor_parcela': 900, 'descricao': 'teste compra 9', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 1000, 'valor_parcela': 1000, 'descricao': 'teste compra 10', 'parcelas': 1, 'user_id': 2, 'banco_id': 1, 'fatura_id': 1},
        {'valor_total': 1100, 'valor_parcela': 1100, 'descricao': 'teste compra 11', 'parcelas': 1, 'user_id': 1, 'banco_id': 1, 'fatura_id': 1},
    ]

    add = 0
    n_add = 0

    for c in compras:
        if not db.session.query(Compras).filter(Compras.valor_total == c['valor_total'], Compras.valor_parcela == c['valor_parcela'], Compras.descricao == c['descricao'], Compras.parcelas == c['parcelas'], Compras.user_id == c['user_id'], Compras.banco_id == c['banco_id'], Compras.fatura_id == c['fatura_id']).first():
            compra = Compras(valor_total=c['valor_total'], valor_parcela=c['valor_parcela'], descricao=c['descricao'], parcelas=c['parcelas'], user_id=c['user_id'], banco_id=c['banco_id'], fatura_id=c['fatura_id'])
            db.session.add(compra)
            add += 1
        else:
            n_add += 1

    db.session.commit()
    if add:
        click.echo(f'{add} Compras adicionadas. {n_add} Compras já existiam')