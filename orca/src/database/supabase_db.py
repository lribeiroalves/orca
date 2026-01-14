import os
from dotenv import load_dotenv
from supabase import create_client, Client
from models import Banco, Saldo, Categoria, Fatura, User, Compra, Conta, Pagamento
from datetime import datetime

# Carrega as variaveis do .env
load_dotenv()

class Database:
    def __init__(self):
        self.__url = os.getenv('SUPABASE_URL')
        self.__key = os.getenv('SUPABASE_API_KEY')

        if not self.__url or not self.__key:
            raise ValueError("Erro: SUPABASE_URL ou SUPABASE_KEY não encontrados no .env")

        # Realiza a conexao com o Supabase
        self.client: Client = create_client(self.__url, self.__key)

    def get_bancos(self) -> list[Banco]:
        try:
            resposta = self.client.table('bancos').select('*').execute()
            # Integracao com o model
            return [Banco.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar bancos: {err}')
            return []
    
    def add_banco(self, banco: str):
        """Recebe um objeto Banco e salva no Database"""
        dados = {
            'nome': banco.upper()
        }
        try:
            return self.client.table('bancos').insert(dados).execute()
        except Exception as e:
            print(e)
            return None
    
    def get_saldos(self, last: bool=False) -> list[Banco]:
        try:
            if not last:
                resposta = self.client.table('saldos').select('id, created_at, bancos(id, nome), saldo').execute()
                return [Saldo.from_json(item) for item in resposta.data]
            else:
                resposta = self.client.rpc('obter_saldos_recentes_com_banco', {}).execute()
                return [Saldo.from_json_last(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar saldos: {err}')
            return []
    
    def add_saldo(self, banco_id: int, saldo: float):
        dados = {
            'banco_id': banco_id,
            'saldo': saldo
        }
        try:
            return self.client.table('saldos').insert(dados).execute()
        except:
            return None
    
    def get_categorias(self) -> list[Categoria]:
        try:
            resposta = self.client.table('categorias_fatura').select('*').order('id', desc=False).execute()
            # Integracao com o model
            return [Categoria.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar categorias: {err}')
            return []
    
    def add_categoria(self, categoria: str):
        dados = {
            'categoria': categoria
        }
        try:
            return self.client.table('categorias_fatura').insert(dados).execute()
        except Exception as e:
            print(e)
            return None
    
    def get_users(self) -> list[User]:
        try:
            resposta = self.client.table('users').select('*').order('id', desc=False).execute()
            # Integracao com o model
            return [User.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar usuarios: {err}')
            return []
    
    def add_user(self, nome: str):
        dados = {
            'nome': nome
        }
        try:
            return self.client.table('users').insert(dados).execute()
        except Exception as e:
            print(e)
            return None
    
    def get_faturas(self) -> list[Fatura]:
        try:
            resposta = self.client.table('faturas').select('id, mes, ano, fatura_paga').order('id', desc=False).execute()
            # Integracao com o model
            return [Fatura.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar faturas: {err}')
            return []
    
    def get_faturas_data(self, mes: int, ano: int):
        try:
            resposta = self.client.table('faturas').select('id, mes, ano, fatura_paga').eq('mes', mes).eq('ano', ano).order('id', desc=False).execute()
            # Integracao com o model
            return [Fatura.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar faturas: {err}')
            return []
    
    def add_fatura(self, mes: int, ano: int, fatura_paga: bool):
        dados = {
            'mes': mes,
            'ano': ano,
            'fatura_paga': fatura_paga
        }
        try:
            return self.client.table('faturas').insert(dados).execute()
        except Exception as e:
            print(e)
            return None
    
    def update_fatura(self, fatura_id: int, status: bool):
        try:
            return self.client.table('faturas').update({'fatura_paga': status}).eq('id', fatura_id).execute()
        except Exception as e:
            print(e)
            return None

    def get_compras(self) -> list[Compra]:
        try:
            resposta = self.client.table('compras').select("""
                id,
                users(id, nome),
                bancos(id, nome),
                faturas(id, mes, ano, fatura_paga),
                categorias_fatura(id, categoria),
                descricao,
                valor_total,
                valor_parcela,
                parcela,
                data_compra,
                hash_compra
            """).order('data_compra', desc=True).execute()
            return [Compra.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar compras: {err}')
            return []
    
    def get_compras_filter(self, ano: str, mes: str, banco: str):
        try:
            resposta = (
                self.client.table('compras').select("""
                    id,
                    users(id, nome),
                    bancos!inner(id, nome),
                    faturas!inner(id, mes, ano, fatura_paga),
                    categorias_fatura(id, categoria),
                    descricao,
                    valor_total,
                    valor_parcela,
                    parcela,
                    data_compra,
                    hash_compra
                """)
                .eq('faturas.ano', int(ano))
                .eq('faturas.mes', int(mes))
                .eq('bancos.id', banco)
                .order('data_compra', desc=True).execute()
            )
            return [Compra.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar compras: {err}')
            return []
    
    def get_compras_hash(self, hash:str):
        try:
            resposta = (
                self.client.table('compras').select("""
                id,
                users(id, nome),
                bancos(id, nome),
                faturas(id, mes, ano, fatura_paga),
                categorias_fatura(id, categoria),
                descricao,
                valor_total,
                valor_parcela,
                parcela,
                data_compra,
                hash_compra
            """)
                .eq('hash_compra', hash)
                .order('data_compra', desc=True).execute()
            )
            return [Compra.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar compras: {err}')
            return []
    
    def add_compra(self, user_id: int, banco_id: int, fatura_id: int, categoria_id: int, descricao: str, valor_total: float, valor_parcela: float, parcela: str, data_compra: datetime, hash_compra: str):
        dados = {
            'user_id': user_id,
            'banco_id': banco_id,
            'fatura_id': fatura_id,
            'categoria_id': categoria_id,
            'descricao': descricao,
            'valor_total': valor_total,
            'valor_parcela': valor_parcela,
            'parcela': parcela,
            'data_compra': data_compra.strftime('%Y-%m-%d'),
            'hash_compra': hash_compra
        }
        try:
            return self.client.table('compras').insert(dados).execute()
        except Exception as e:
            print(e)
            return None

    def delete_compra_hash(self, h:str):
        try:
            return (
                self.client.table('compras')
                .delete()
                .eq('hash_compra', h)
                .execute()
            )
        except Exception as e:
            print(e)
            return None
    
    def get_contas(self) -> list[Conta]:
        try:
            resposta = self.client.table('contas').select('*').order('id', desc=False).execute()
            # Integracao com o model
            return [Conta.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar contas: {err}')
            return []
    
    def get_contas_or(self, mes: int):
        try:
            resposta = (
                self.client.table('contas')
                .select('*')
                .or_(f'mensal.eq.true, anual.eq.{mes}' )
                .order('id', desc=False)
                .execute())
            # Integracao com o model
            return [Conta.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar contas: {err}')
            return []
    
    def get_contas_desc(self, desc: str):
        try:
            resposta = self.client.table('contas').select('*').eq('desc', desc).order('id', desc=False).execute()
            # Integracao com o model
            return [Conta.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar contas: {err}')
            return []
    
    def add_conta(self, desc: str, mensal: bool, anual: int):
        dados = {
            'desc': desc,
            'mensal': mensal,
            'anual': anual
        }
        try:
            return self.client.table('contas').insert(dados).execute()
        except Exception as e:
            print(e)
            return None

    
    def get_pagamentos(self) -> list[Pagamento]:
        try:
            resposta = self.client.table('pagamentos').select("""
                id,
                faturas(id, mes, ano),
                contas(id, desc, mensal, anual),
                valor,
                pago
            """).order('id', desc=False).execute()
            return [Compra.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar pagamentos: {err}')
            return []
    
    def get_pagamentos_date(self, ano: int, mes: int):
        try:
            resposta = (self.client.table('pagamentos').select("""
                id,
                faturas!inner(id, mes, ano),
                contas(id, desc, mensal, anual),
                valor,
                pago
            """)
            .eq('faturas.ano', ano)
            .eq('faturas.mes', mes)
            .order('id', desc=False).execute())
            return [Pagamento.from_json(item) for item in resposta.data]
        except Exception as err:
            print(f'Erro ao buscar pagamentos: {err}')
            return []
    
    def add_pagamento(self, fatura_id: int, conta_id: int, valor: float, pago: bool):
        dados = {
            'fatura_id': fatura_id,
            'conta_id': conta_id,
            'valor': valor,
            'pago': pago
        }
        try:
            return self.client.table('pagamentos').insert(dados).execute()
        except Exception as e:
            print(e)
            return None
    
    def update_pagamento(self, id: int, valor: float, status: bool):
        dados = {
            'valor': valor,
            'pago': status
        }
        try:
            return self.client.table('pagamentos').update(dados).eq('id', id).execute()
        except Exception as e:
            print(e)
            return None