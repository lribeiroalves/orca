from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, StringField, HiddenField
from wtforms.validators import DataRequired
from datetime import datetime

from app.ext.database import db
from app.ext.database.models import *


class FormCompra(FlaskForm):
    userCompra = SelectField('Usuário', choices=[], validators=[DataRequired()])
    bancoCompra = SelectField('Banco', choices=[], validators=[DataRequired()])
    faturaCompra = SelectField('Fatura', description='Aguardando a data da compra.', choices=[('', '...')], validators=[DataRequired()])
    valorCompra = StringField('Valor', validators=[DataRequired()])
    parcelaCompra = StringField('Parcelas', validators=[DataRequired()])
    categoriaCompra = SelectField('Categoria', choices=[], validators=[DataRequired()])
    descCompra = TextAreaField('Descrição', validators=[DataRequired()], render_kw={'rows': 5, 'style': 'height: 100%;'})
    dataCompra = StringField('Data da Compra', validators=[DataRequired()])
    hashCompra = HiddenField('hashCompra', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            users = db.session.scalars(db.select(Users)).all()
            self.userCompra.choices = [(str(u.id), str(u.nome).title()) for u in users]
            self.userCompra.choices.insert(0, ('', 'Selecione...'))

            bancos = db.session.scalars(db.select(Bancos).where(Bancos.cartao == True)).all()
            self.bancoCompra.choices = [(str(b.id), str(b.nome).title()) for b in bancos]
            self.bancoCompra.choices.insert(0, ('', 'Selecione...'))

            categorias = db.session.scalars(db.select(Categorias)).all()
            self.categoriaCompra.choices = [(str(c.id), str(c.nome).title()) for c in categorias]
            self.categoriaCompra.choices.insert(0, ('', 'Selecione...'))


class FormSaldos(FlaskForm):
    userSaldo = SelectField('Usuário', choices=[], validators=[DataRequired()])
    anoSaldo = StringField('Ano', validators=[DataRequired()])
    mesSaldo = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired()])
    valorSaldo = StringField('Valor', validators=[DataRequired()])
    idSaldo = HiddenField('idSaldo', validators=[DataRequired()])
    bancoSaldo = SelectField('Banco', choices=[], validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = db.session.scalars(db.select(Users)).all()
        self.userSaldo.choices = [(str(u.id), str(u.nome).title()) for u in users]
        self.userSaldo.choices.insert(0, ('', 'Selecione...'))

        bancos = db.session.scalars(db.select(Bancos)).all()
        self.bancoSaldo.choices = [(str(b.id), str(b.nome).title()) for b in bancos]
        self.bancoSaldo.choices.insert(0, ('', 'Selecione...'))


class FormExcluir(FlaskForm):
    idExcluir = HiddenField('idExcluir', validators=[DataRequired()])
    tipoExcluir = HiddenField('tipoExcluir', validators=[DataRequired()])
    anoExcluir = HiddenField('anoExcluir', validators=[DataRequired()])
    mesExcluir = HiddenField('mesExcluir', validators=[DataRequired()])
    userExcluir = HiddenField('userExcluir', validators=[DataRequired()])


class FormEntradaSaida(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired()])
    ano = StringField('Ano', validators=[DataRequired()])
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired()])
    desc = TextAreaField('Descrição', validators=[DataRequired()], render_kw={'rows': 5, 'style': 'height: 100%;'})
    valor = StringField('Valor', validators=[DataRequired()])
    form_name = HiddenField('formInOutName', validators=[DataRequired()])
    idInOut = HiddenField('idInOut', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = db.session.scalars(db.select(Users)).all()
        self.user.choices = [(str(u.id), str(u.nome).title()) for u in users]
        self.user.choices.insert(0, ('', 'Selecione...'))


class FormFiltroTabelas(FlaskForm):
    user = SelectField('Usuário', choices=[], validators=[DataRequired()])
    ano = SelectField('Ano', choices=[], validators=[DataRequired()], default=datetime.now().year, validate_choice=False)
    mes = SelectField('Mês', choices=[('', 'Selecione...'), ('1', 'Janeiro'), ('2', 'Fevereiro'), ('3', 'Março'), ('4', 'Abril'), ('5', 'Maio'), ('6', 'Junho'), ('7', 'Julho'), ('8', 'Agosto'), ('9', 'Setembro'), ('10', 'Outubro'), ('11', 'Novembro'), ('12', 'Dezembro')], validators=[DataRequired()], default=datetime.now().month)
    form_name = HiddenField('form_name')
    tipo = HiddenField('tipo')
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = db.session.scalars(db.select(Users)).all()
        self.user.choices = [(str(u.id), str(u.nome).title()) for u in users]
        self.user.choices.insert(0, ('', 'Selecione...'))

        anos_entradas = db.session.scalars(db.select(Entradas.ano)).all()
        anos_saidas = db.session.scalars(db.select(Saidas.ano)).all()
        anos_saldos = db.session.scalars(db.select(Saldos.ano)).all()
        anos = list(set(anos_entradas) | set(anos_saldos) | set(anos_saidas))
        self.ano.choices = [(str(ano), str(ano)) for ano in anos]
        self.ano.choices.insert(0, ('', 'Selecione...'))