from dataclasses import dataclass
from datetime import datetime

@dataclass
class Categoria:
    id: int
    categoria: str

    @classmethod
    def from_json(cls, data:dict):
        return cls(
            id=data.get('id'),
            categoria=data.get('categoria')
        )
