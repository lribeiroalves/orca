import os
from dotenv import load_dotenv
from supabase import create_client, Client
from models import Banco, Saldo
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
        except:
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