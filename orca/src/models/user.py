from dataclasses import dataclass

@dataclass
class User:
    id: int
    nome: str

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            id = data.get('id'),
            nome = data.get('nome')
        )