from dataclasses import dataclass
from datetime import datetime


@dataclass
class Compra:
    id: int
    user_id: int
    user_nome: str
    banco_id: int
    banco_nome: str
    fatura_id: int
    fatura_str: str
    categoria_id: int
    categoria_nome: str
    descricao: str
    valor_total: float
    valor_parcela: float
    parcela: str
    data_compra: datetime

    @classmethod
    def from_json(cls, data: dict):
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        return cls(
            id = data.get('id'),
            user_id = data.get('users')['id'],
            user_nome = data.get('users')['nome'],
            banco_id = data.get('bancos')['id'],
            banco_nome = data.get('bancos')['nome'],
            fatura_id = data.get('faturas')['id'],
            fatura_str = f'{meses[data.get("faturas")["mes"] - 1]} / {data.get("faturas")["ano"]}',
            categoria_id = data.get(data.get('categorias_fatura')['id']),
            categoria_nome = data.get('categorias_fatura')['categoria'],
            descricao = data.get('descricao'),
            valor_total = data.get('valor_total'),
            valor_parcela = data.get('valor_parcela'),
            parcela = data.get('parcela'),
            data_compra = datetime.strptime(data.get('data_compra'), '%Y-%m-%d'),
        )