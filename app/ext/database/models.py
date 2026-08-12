from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from . import db


class Users(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Usuario(id: {self.id}, nome: {self.nome})'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }
