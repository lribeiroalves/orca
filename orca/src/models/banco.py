from dataclasses import dataclass

@dataclass
class Banco:
    id: int
    nome: str

    @classmethod
    def from_json(cls, data: dict):
        """Converte o dicionario do Supabase em um Objeto Python"""
        return cls(
            id=data.get('id'),
            nome = data.get('nome')
        )