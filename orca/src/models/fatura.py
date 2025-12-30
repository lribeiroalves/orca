from dataclasses import dataclass
from datetime import datetime

@dataclass
class Fatura:
    id: int
    mes: int
    mes_str: str
    ano: int
    status_ok: bool

    @classmethod
    def from_json(cls, data:dict):
        meses = [
            "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"
        ]
        return cls(
            id = data.get('id'),
            mes = data.get('mes'),
            mes_str = meses[data.get('mes') - 1],
            ano = data.get('ano'),
            status_ok = data.get('status_ok')
        )
