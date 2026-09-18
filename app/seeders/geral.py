import click
import random
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Ajuste os imports abaixo conforme a estrutura do seu projeto
from app.ext.database import db
from app.ext.database.models import *

@click.command('seed-geral')
def seed_geral():
    """Popula o banco de dados com dados simulados para desenvolvimento."""
    
    try:
        # 1. Criar Usuários
        nomes_usuarios = ['lucas', 'ribeiro', 'alves']
        users = []
        for nome in nomes_usuarios:
            u = Users(nome=nome)
            db.session.add(u)
            users.append(u)
        
        # 2. Criar Bancos (5 bancos, apenas 2 com cartão)
        bancos_data = [
            {'nome': 'Nubanko', 'cartao': True},
            {'nome': 'Banco Intermedium', 'cartao': True},
            {'nome': 'Itaúna', 'cartao': False},
            {'nome': 'Banco do Brasilia', 'cartao': False},
            {'nome': 'Caixa Econômica', 'cartao': False}
        ]
        bancos = []
        bancos_cartao = []
        for b_data in bancos_data:
            b = Bancos(nome=b_data['nome'], cartao=b_data['cartao'])
            db.session.add(b)
            bancos.append(b)
            if b_data['cartao']:
                bancos_cartao.append(b)

        # 3. Criar Categorias
        nomes_categorias = ['Alimentação', 'Transporte', 'Lazer', 'Moradia', 'Esportes', 'Diversos']
        categorias = []
        for c_nome in nomes_categorias:
            c = Categorias(nome=c_nome)
            db.session.add(c)
            categorias.append(c)

        # Commit inicial para garantir que IDs existam para as relações abaixo
        db.session.commit() 

        # 4. Gerar dados mensais (Janeiro a Junho de 2026)
        ano_base = 2026
        meses = range(1, 7)

        for mes in meses:
            # Criar Fatura central do mês
            fatura = Faturas(ano=ano_base, mes=mes, status_paga=False)
            db.session.add(fatura)

            for user in users:
                # Gerar Saldos: Para TODOS os bancos, TODOS os usuários, em CADA mês
                for banco in bancos:
                    # ~50% de chance de ter saldo zerado naquele banco, caso contrário um valor aleatório
                    valor_saldo = round(random.uniform(100, 5000), 2) if random.random() > 0.5 else 0.0
                    saldo = Saldos(ano=ano_base, mes=mes, valor=valor_saldo, user=user, banco=banco)
                    db.session.add(saldo)

                # Gerar Entradas (ex: Salário fixo mensal)
                entrada = Entradas(
                    ano=ano_base, 
                    mes=mes, 
                    descricao=f'Salário Mensal {mes:02d}/{ano_base}', 
                    valor=round(random.uniform(3000, 8000), 2), 
                    user=user
                )
                db.session.add(entrada)

                # Gerar Saídas em dinheiro/Pix (ex: Contas recorrentes)
                descricoes_saida = ['Conta de Luz', 'Conta de Água', 'Internet', 'Mensalidade Jiu-Jitsu', 'Aluguel']
                for _ in range(random.randint(1, 3)):
                    saida = Saidas(
                        ano=ano_base,
                        mes=mes,
                        descricao=random.choice(descricoes_saida),
                        valor=round(random.uniform(50, 800), 2),
                        user=user
                    )
                    db.session.add(saida)

                # Gerar Compras no Cartão de Crédito
                descricoes_compras = ['Supermercado', 'iFood', 'Uber', 'Farmácia', 'Posto de Gasolina', 'Lego', 'Livros da faculdade']
                for _ in range(random.randint(2, 5)):
                    valor_total = round(random.uniform(30, 1000), 2)
                    parcelas = random.choice([1, 1, 1, 2, 3, 10]) # Maior peso para compras à vista
                    valor_parcela = round(valor_total / parcelas, 2)
                    
                    compra = Compras(
                        valor_total=valor_total,
                        valor_parcela=valor_parcela,
                        descricao=random.choice(descricoes_compras),
                        parcelas=parcelas,
                        data=datetime(ano_base, mes, random.randint(1, 28)),
                        hash=f'tx_{user.id}{mes}{random.randint(1000,9999)}',
                        user=user,
                        banco=random.choice(bancos_cartao), # Relacionado APENAS a bancos com cartão
                        fatura=fatura,
                        categoria=random.choice(categorias)
                    )
                    db.session.add(compra)

        db.session.commit()
        click.echo('✅ Banco de dados populado com sucesso para desenvolvimento!')

    except IntegrityError:
        db.session.rollback()
        click.echo('❌ Erro de integridade: O banco já contém dados que conflitam com as chaves únicas (ex: Saldos do mesmo ano/mês). Limpe o banco antes de rodar o seed novamente.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'❌ Erro inesperado ao popular o banco: {e}')


def init_app(app):
    # Adicionando o novo comando junto com os outros (se aplicável)
    if app.config['ENV'] == 'development':
        app.cli.add_command(seed_geral)