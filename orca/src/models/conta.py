from dataclasses import dataclass

@dataclass
class Conta:
    id: int
    desc: str
    mensal: bool
    anual: int

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            id = data.get('id'),
            desc = data.get('desc'),
            mensal = data.get('mensal'),
            anual = data.get('anual')
        )