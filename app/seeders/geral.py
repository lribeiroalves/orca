import click
import json
import hashlib
import random
from datetime import datetime
from sqlalchemy.exc import IntegrityError

# Certifique-se de importar o db e as models a partir do módulo correto no seu projeto
from app.ext.database import db 
from app.ext.database.models import Users, Entradas, Saidas, Bancos, Saldos, Faturas, Categorias, Compras

@click.command('seed-geral')
def seed_geral():
    click.echo('Iniciando o processo de seeding geral...')
    
    # 1. Limpeza de dados (Opcional, mas recomendado para evitar duplicação em múltiplos testes)
    try:
        db.session.query(Compras).delete()
        db.session.query(Saldos).delete()
        db.session.query(Entradas).delete()
        db.session.query(Saidas).delete()
        db.session.query(Faturas).delete()
        db.session.query(Categorias).delete()
        db.session.query(Bancos).delete()
        db.session.query(Users).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        click.echo(f'Aviso durante limpeza de banco: {e}')

    # 2. Usuários
    nomes_usuarios = ['lucas', 'ribeiro', 'alves']
    users = []
    for nome in nomes_usuarios:
        user = Users(nome=nome)
        db.session.add(user)
        users.append(user)
    db.session.flush() # flush para gerar os IDs sem commitar

    # 3. Bancos
    # 5 bancos parecidos com os reais, sendo apenas 2 com cartão = True
    bancos_info = [
        ("Nubank", True),
        ("Itaú Unibanco", True),
        ("Caixa Econômica", False),
        ("Banco Bradesco", False),
        ("Banco do Brasil", False)
    ]
    bancos = []
    bancos_cartao = []
    for nome, cartao in bancos_info:
        banco = Bancos(nome=nome, cartao=cartao)
        db.session.add(banco)
        bancos.append(banco)
        if cartao:
            bancos_cartao.append(banco)
    db.session.flush()

    # 4. Categorias
    cat_nomes = ["Alimentação", "Moradia", "Lazer", "Transporte", "Saúde", "outros"]
    categorias = []
    categorias_dict = {}
    for nome in cat_nomes:
        cat = Categorias(nome=nome)
        db.session.add(cat)
        categorias.append(cat)
        categorias_dict[nome] = cat
    db.session.flush()

    # 5. Faturas (Jan/2026 até Dez/2028)
    anos = [2026, 2027, 2028]
    meses = list(range(1, 13))
    faturas_dict = {}
    for ano in anos:
        for mes in meses:
            fatura = Faturas(ano=ano, mes=mes, status_paga=True)
            db.session.add(fatura)
            db.session.flush()
            faturas_dict[(ano, mes)] = fatura

    # 6. Entradas, Saídas e Saldos
    # Rastreador de saldos: {user_id: {banco_id: saldo_atual}}
    user_balances = {u.id: {} for u in users}
    
    # Cada usuário terá um banco "principal" de movimentação para receber salário e pagar contas base
    user_main_bank = {
        users[0].id: bancos[0], # lucas -> Nubank
        users[1].id: bancos[2], # ribeiro -> Caixa
        users[2].id: bancos[3]  # alves -> Bradesco
    }
    
    # Inicializando as contas principais
    for u in users:
        user_balances[u.id][user_main_bank[u.id].id] = 0.0

    # População mensal das movimentações básicas de uma residência
    for ano in anos:
        for mes in meses:
            for u in users:
                banco_principal = user_main_bank[u.id]

                # ENTRADA: Salário base (flutua um pouco para não ser robótico)
                salario = round(random.uniform(4500.00, 6000.00), 2)
                db.session.add(Entradas(ano=ano, mes=mes, descricao="Salário Mensal", valor=salario, user_id=u.id))

                # SAÍDAS: Gastos coerentes de uma casa
                aluguel = 1200.00
                db.session.add(Saidas(ano=ano, mes=mes, descricao="Aluguel", valor=aluguel, user_id=u.id))

                energia = round(random.uniform(150.00, 220.00), 2)
                db.session.add(Saidas(ano=ano, mes=mes, descricao="Conta de Luz", valor=energia, user_id=u.id))

                mercado = round(random.uniform(700.00, 1100.00), 2)
                db.session.add(Saidas(ano=ano, mes=mes, descricao="Supermercado Atacadão", valor=mercado, user_id=u.id))

                net_mensal = salario - aluguel - energia - mercado
                user_balances[u.id][banco_principal.id] += net_mensal

                # Evento eventual: Dezembro tem 13º salário caindo num banco diferente, ativando ele pra sempre
                if mes == 12:
                    banco_extra = bancos[4] # Banco do Brasil
                    decimo_terceiro = round(salario / 2, 2)
                    db.session.add(Entradas(ano=ano, mes=mes, descricao="13º Salário (Parcela)", valor=decimo_terceiro, user_id=u.id))
                    
                    if banco_extra.id not in user_balances[u.id]:
                        user_balances[u.id][banco_extra.id] = 0.0
                    user_balances[u.id][banco_extra.id] += decimo_terceiro

                # SALDOS: Atualizando para todos os bancos que o usuário JÁ TEVE saldo histórico
                for b_id, saldo_atual in user_balances[u.id].items():
                    db.session.add(Saldos(
                        ano=ano, mes=mes, 
                        valor=round(saldo_atual, 2), 
                        user_id=u.id, 
                        banco_id=b_id
                    ))

    db.session.flush()

    # 7. Compras
    def gerar_hash_compra(user_id, banco_id, categoria_id, data_obj, mes_fat, ano_fat, valor, parcelas, desc):
        """Função espelho da sua view formValidate para garantir o match exato do hashcode"""
        dados = {
            'user': str(user_id), # Formulário WTForms com SelectField costuma enviar string antes do cast
            'banco': int(banco_id),
            'categoria': int(categoria_id),
            'data': data_obj,
            'mes_fatura': int(mes_fat),
            'ano_fatura': int(ano_fat),
            'valor': float(valor),
            'parcelas': int(parcelas),
            'desc': desc,
            'hash': '0',
        }
        string_padronizada = json.dumps(dados, sort_keys=True, default=str)
        return hashlib.sha256(string_padronizada.encode('utf-8')).hexdigest()

    # Catálogo de compras verossímeis
    compras_ficticias = [
        ("Smart TV Samsung", 2500.00, 10, "Lazer"),
        ("Geladeira Brastemp", 3200.00, 12, "Moradia"),
        ("Cadeira de Escritório", 800.00, 4, "outros"),
        ("Tênis Nike", 350.00, 2, "Saúde"),
        ("Compra Mensal Assaí", 900.00, 1, "Alimentação"),
        ("Pneus Carro", 1400.00, 4, "Transporte")
    ]

    for u in users:
        # Pega um banco aleatório com cartão para as faturas
        banco_cartao = random.choice(bancos_cartao)
        
        # Sorteia algumas compras ao longo dos anos
        for _ in range(5): 
            desc, valor_t, qtd_parcelas, cat_nome = random.choice(compras_ficticias)
            categoria_id = categorias_dict[cat_nome].id
            
            ano_c = random.choice([2026, 2027, 2028])
            mes_c = random.randint(1, 12)
            dia_c = random.randint(1, 28)
            data_compra = datetime(ano_c, mes_c, dia_c)

            # Assumindo que a fatura inicial seja a do mês seguinte da compra
            mes_fat_inicial = mes_c + 1 if mes_c < 12 else 1
            ano_fat_inicial = ano_c if mes_c < 12 else ano_c + 1

            hashcode = gerar_hash_compra(
                u.id, banco_cartao.id, categoria_id, data_compra,
                mes_fat_inicial, ano_fat_inicial, valor_t, qtd_parcelas, desc
            )

            valor_parcela = round(valor_t / qtd_parcelas, 2)

            for i in range(1, qtd_parcelas + 1):
                m_fat = mes_fat_inicial + i - 1
                a_fat = ano_fat_inicial
                
                # Ajusta se as parcelas virarem o ano
                while m_fat > 12:
                    m_fat -= 12
                    a_fat += 1

                # Se a parcela cair em anos futuros (ex: 2029+), cria a fatura dinamicamente
                if (a_fat, m_fat) not in faturas_dict:
                    fatura_nova = Faturas(ano=a_fat, mes=m_fat, status_paga=False)
                    db.session.add(fatura_nova)
                    db.session.flush()
                    faturas_dict[(a_fat, m_fat)] = fatura_nova
                
                fat = faturas_dict[(a_fat, m_fat)]
                
                # Regra: parcela atual * 100 + numero de parcelas
                # Exemplo: 5ª parcela de 12 = (5 * 100) + 12 = 512
                col_parcela = (i * 100) + qtd_parcelas 

                compra = Compras(
                    valor_total=valor_t,
                    valor_parcela=valor_parcela,
                    descricao=desc,
                    parcelas=col_parcela,
                    data=data_compra,
                    hash=hashcode,
                    user_id=u.id,
                    banco_id=banco_cartao.id,
                    fatura_id=fat.id,
                    categoria_id=categoria_id
                )
                db.session.add(compra)

    # Commit final com todas as operações
    db.session.commit()
    click.echo('✅ Banco populado com sucesso (seed-geral)!')