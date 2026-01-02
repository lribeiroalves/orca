import os
from dotenv import load_dotenv
from supabase import create_client, Client
from models import Banco, Saldo, Categoria, Fatura, User, Compra
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
                data_compra
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
                    data_compra
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
    
    def add_compra(self, user_id: int, banco_id: int, fatura_id: int, categoria_id: int, descricao: str, valor_total: float, valor_parcela: float, parcela: str, data_compra: datetime):
        dados = {
            'user_id': user_id,
            'banco_id': banco_id,
            'fatura_id': fatura_id,
            'categoria_id': categoria_id,
            'descricao': descricao,
            'valor_total': valor_total,
            'valor_parcela': valor_parcela,
            'parcela': parcela,
            'data_compra': data_compra.strftime('%Y-%m-%d')
        }
        try:
            return self.client.table('compras').insert(dados).execute()
        except Exception as e:
            print(e)
            return None

    # def popular_compras(self):
    #     import pickle
    #     # Carrega o dicionário do arquivo
    #     with open('df_c_data_corrigida.pkl', 'rb') as arquivo:
    #         dados_carregados = pickle.load(arquivo)

    #     try:
    #         resposta = self.client.table('compras').insert(dados_carregados).execute()
    #         print(f'{len(resposta)} registros Salvos com Sucesso.')
    #         return resposta
    #     except Exception as e:
    #         print(e)
    #         return None
