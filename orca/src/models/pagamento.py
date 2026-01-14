from dataclasses import dataclass

@dataclass
class Pagamento:
    id: int
    fatura_id: int
    fatura_mes: int
    fatura_ano: int
    conta_id: int
    conta_desc: str
    conta_mensal: bool
    conta_anual: int
    valor: float
    pago: bool

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            id = data.get('id'),
            fatura_id = data.get('faturas')['id'],
            fatura_mes = data.get('faturas')['mes'],
            fatura_ano = data.get('faturas')['ano'],
            conta_id = data.get('contas')['id'],
            conta_desc = data.get('contas')['desc'],
            conta_mensal = data.get('contas')['mensal'],
            conta_anual = data.get('contas')['anual'],
            valor = data.get('valor'),
            pago = data.get('pago')
        )