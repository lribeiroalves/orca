from sqlalchemy import String, Numeric, DateTime, Boolean, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class Entradas(db.Model):
    __table_args__ = (
        CheckConstraint("ano >= 2026", name="check_ano_valido"),
        CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes_valido"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # Relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')

    def __repr__(self):
        return f'Entrada(id: {self.id}, ano: {self.ano}, mes: {self.mes}, descricao: {self.descricao}, valor: {self.valor}, user_id: {self.user_id}, user: {self.user})'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'descricao': self.descricao,
            'valor': self.valor,
            'user_id': self.user_id
        }


class Saidas(db.Model):
    __table_args__ = (
        CheckConstraint("ano >= 2026", name="check_ano_v"),
        CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes_v"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # Relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')

    def __repr__(self):
        return f'Saida(id: {self.id}, ano: {self.ano}, mes: {self.mes}, descricao: {self.descricao}, valor: {self.valor}, user_id: {self.user_id}, user: {self.user})'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'descricao': self.descricao,
            'valor': self.valor,
            'user_id': self.user_id
        }


class Bancos(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Banco(id: {self.id}, nome: {self.nome})'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }


class Saldos(db.Model):
    __table_args__ = (
            CheckConstraint("ano >= 2026", name="check_ano"),
            CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes"),
            UniqueConstraint('ano', 'mes', 'banco_id', 'user_id', name='unique_ano_mes_banco_user')
        )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)

    # relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')
    banco_id: Mapped[int] = mapped_column(ForeignKey('bancos.id'))
    banco: Mapped['Bancos'] = relationship('Bancos')

    def __repr__(self):
        return f'valor(id: {self.id}, ano: {self.ano}, mes: {self.mes}, valor: {self.valor}, user_id: {self.user_id}, user: {self.user}, banco_id: {self.banco_id}, banco: {self.banco})'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'valor': self.valor,
            'user_id': self.user_id,
            'banco_id': self.banco_id
        }


class Faturas(db.Model):
    __table_args__ = (
                CheckConstraint("ano >= 2026", name="check_ano_fatura"),
                CheckConstraint("mes >= 1 AND mes <= 12", name="check_mes_fatura"),
                CheckConstraint("status_paga IN (0,1)", name="check_bool"),
            )

    id: Mapped[int] = mapped_column(primary_key=True)
    ano: Mapped[int] = mapped_column(nullable=False)
    mes: Mapped[int] = mapped_column(nullable=False)
    status_paga: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'Fatura(id: {self.id}, ano: {self.ano}, mes: {self.mes}, status_paga: {self.status_paga})'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'mes': self.mes,
            'status_paga': self.status_paga
        }


class Categorias(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f'Categoria(id: {self.id}, nome: {self.nome})'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome
        }


class Compras(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    valor_total: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    valor_parcela: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    parcelas: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[DateTime] = mapped_column(DateTime)

    # relacoes
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['Users'] = relationship('Users')
    banco_id: Mapped[int] = mapped_column(ForeignKey('bancos.id'))
    banco: Mapped['Bancos'] = relationship('Bancos')
    fatura_id: Mapped[int] = mapped_column(ForeignKey('faturas.id'))
    fatura: Mapped['Faturas'] = relationship('Faturas')
    categoria_id: Mapped[int] = mapped_column(ForeignKey('categorias.id'))
    categoria: Mapped['Categorias'] = relationship('Categorias')

    def __repr__(self):
        return f'Compra(id: {self.id}, valor_total: {self.valor_total}, valor_parcela: {self.valor_parcela}, descricao: {self.descricao}, parcelas: {self.parcelas}, user_id: {self.user_id}, user: {self.user}, banco_id: {self.banco_id}, banco: {self.banco}, fatura_id: {self.fatura_id}, fatura: {self.fatura}), data: {self.data}'

    def to_dict(self):
        return {
            'id': self.id,
            'valor_total': self.valor_total,
            'valor_parcela': self.valor_parcela,
            'descricao': self.descricao,
            'parcelas':self.parcelas,
            'user_id': self.user_id,
            'banco_id': self.banco_id,
            'fatura_id': self.fatura_id,
            'data': self.data,
        }