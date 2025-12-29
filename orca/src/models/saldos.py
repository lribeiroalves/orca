from dataclasses import dataclass
from datetime import datetime

@dataclass
class Saldo:
    id: int
    date: datetime
    saldo: float
    banco_id: int
    banco_nome: str

    @classmethod
    def from_json(cls, data: dict):
        """Converte o dicionario do Supabase em um Objeto Python"""
        return cls(
            id=data.get('id'),
            date = datetime.strptime(data.get('created_at'), '%Y-%m-%d'),
            saldo = data.get('saldo'),
            banco_id = data.get('bancos')['id'],
            banco_nome = data.get('bancos')['nome']
        )