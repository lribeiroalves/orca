import flet as ft
from database import Database
from typing import Callable
from models import Fatura, Categoria, Banco, Conta
from datetime import datetime
import uuid


class MyButton(ft.ElevatedButton):
    def __init__(self, text: str, page: ft.Page, route: str, enable: bool=True):
        super().__init__()
        if enable:
            self.bgcolor = ft.Colors.BLUE_900
        else:
            self.bgcolor = ft.Colors.BLACK38
            self.disabled = True
        self.color = ft.Colors.WHITE
        self.text = text
        self.on_click = lambda _: page.go(route)


class MyAppBar(ft.AppBar):
    def __init__(self, text: str, page: ft.Page):
        super().__init__()
        self.leading = ft.Icon(ft.Icons.ATTACH_MONEY_ROUNDED)
        self.leading_width = 50
        self.title = ft.Text(text, size=16)
        self.center_title = False
        self.bgcolor = ft.Colors.BLACK87
        self.color = ft.Colors.WHITE
        self.btn_back = ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.on_view_pop(None))
        self.actions = [
            self.btn_back,
            ft.IconButton(ft.Icons.HOME_OUTLINED, on_click=lambda _: page.go('/')),
            ft.Container(width=20)
        ]
        if len(page.views) < 3:
            self.btn_back.visible = False


class MyWarnings:
    # Banner para ser exibido quando houver erro de conexao com o Supabase
    banner_conexao = None

    def __init__(self):
        raise SyntaxError("Esta classe não deve ser instanciada. Use os métodos diretamente.")

    @classmethod
    def abrir_banner_conexao(cls, page: ft.Page):
        cls.banner_conexao = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                value='Nao foi possivel se conectar ao Supabase, verifique se o projeto esta pausado.',
                color=ft.Colors.BLACK
            ),
            actions=[
                ft.TextButton(
                    text='OK', style=ft.ButtonStyle(color=ft.Colors.BLUE), on_click=lambda e: cls.fechar_banner_conexao(page)
                ),
            ],
        )
        page.open(cls.banner_conexao)
    
    @classmethod
    def fechar_banner_conexao(cls, page):
        page.close(cls.banner_conexao)
    

class MyPopup:
    def __init__(self, titulo: str, function: Callable, page: ft.Page):
        self.page = page
        self.popup = ft.AlertDialog(
                title=ft.Text('Confirmação'),
                content=ft.Text(titulo),
                actions=[
                    # ft.TextButton('Cancela', on_click=lambda _: self.fechar_popup),
                    ft.ElevatedButton('Confirma', bgcolor=ft.Colors.BLUE_900, color='white', on_click=self.confirmar_acao(function))
                ]
            )
    
    def fechar_popup(self, _):
        self.popup.open = False
        self.page.update()
    
    def confirmar_acao(self, func):
        def wrapper(e):
            func(e)
            self.fechar_popup(None)
        return wrapper


class MyBsAddCompra:
    def __init__(self, p: ft.Page, faturas: list[Fatura], categorias: list[Categoria], bancos: list[Banco], db: Database):
        self.page = p

        self.title = 'Cadastrar Compra'

        self.faturas = faturas
        self.db = db

        self.txt_data = ft.TextField(label='Data da Compra', read_only=True, on_focus=self.__open_calendar)
        self.calendar = ft.DatePicker(on_change=self.__on_change_calendar, on_dismiss=self.__on_dismiss_calendar, date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY, )

        self.txt_parcela = ft.TextField(label='Parcelas', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter())

        self.reg_str = r"^(|-|(-?[0-9]+([.,][0-9]{0,2})?))$"
        self.txt_valorTotal = ft.TextField(label='Valor Total', prefix_text='R$ ', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = self.reg_str, allow=True, replacement_string=""))

        self.txt_desc = ft.TextField(label='Descrição', multiline=True, min_lines=4, max_lines=4, align_label_with_hint=True)

        self.opt_user = [ft.DropdownOption(key='1', content=ft.Text('Lucas'), text='Lucas'), ft.DropdownOption(key='2', content=ft.Text('Selma'), text='Selma'), ft.DropdownOption(key='3', content=ft.Text('Ambos'), text='Ambos')]
        self.dd_user = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Usuário', options=self.opt_user, expand=True, width=500)

        self.opt_banco = [ft.DropdownOption(key=b.id, content=b.nome, text=b.nome) for b in bancos]
        self.dd_banco = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Banco', options=self.opt_banco, expand=True, width=500)

        self.opt_cat = [ft.DropdownOption(key=c.id, content=c.categoria, text=c.categoria) for c in categorias]
        self.dd_cat = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Categoria', options=self.opt_cat, expand=True, width=500)

        self.txt_mesFatura = ft.TextField(label='Mês da Fatura', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = r"^[0-9]{0,2}$", allow=True, replacement_string=""), hint_text='Ex: 02', value=datetime.now().strftime('%m'))
        self.txt_anoFatura = ft.TextField(label='Ano da Fatura', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = r"^[0-9]{0,4}$", allow=True, replacement_string=""), hint_text='Ex: 2025', value=datetime.now().strftime('%Y'))

        self.btn_confirma = ft.ElevatedButton('Cadastrar', bgcolor=ft.Colors.BLUE_900, color='white', elevation=4, col={'xs': 10, 'md': 6}, on_click=self.abrir_confirmacao)
        self.txt_pos_confirma = ft.Text('Voce confirma o cadastro dessa compra?', col={'xs': 12}, visible=False)
        self.btn_pos_cancela = ft.ElevatedButton('Cancelar', bgcolor=ft.Colors.RED_900, color='white', elevation=4, col={'xs': 6, 'md': 6}, on_click=self.cancelar_confirmacao)
        self.btn_pos_confirma = ft.ElevatedButton('Confirmar', bgcolor=ft.Colors.BLUE_900, color='white', elevation=4, col={'xs': 6, 'md': 6}, on_click=self.confirmar_cadastro)

        self.linha_cadastro = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.btn_confirma
            ],
            visible=True
        )
        self.linha_confirmacao = ft.ResponsiveRow(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.txt_pos_confirma,
                self.btn_pos_cancela,
                self.btn_pos_confirma,
                # ft.Divider(height=10, color='transparent')
            ],
            visible=False
        )

        self.bs = ft.BottomSheet(
            ft.Column([
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    col={'xs': 8, 'md': 6},
                                    content=ft.Text(self.title, size=20, weight='bold')
                                ),
                                ft.Container(
                                    col={'xs': 4, 'md': 4},
                                    content=ft.ElevatedButton(' Limpar ', on_click=self.limpar_bs,bgcolor=ft.Colors.BLUE_300, color='white')
                                ),
                            ]
                        ),
                        ft.Divider(height=15, color='transparent'),
                        ft.ResponsiveRow(
                            controls=[
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.txt_anoFatura
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.txt_mesFatura
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.dd_banco
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.txt_data
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.txt_valorTotal
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.txt_parcela
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.dd_cat
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.dd_user
                                ),
                            ]
                        ),
                        self.txt_desc,
                        ft.Divider(height=10, thickness=1, color='grey'),
                        self.linha_cadastro,
                        self.linha_confirmacao
                    ], tight=True)
                )], scroll=ft.ScrollMode.AUTO,
            ), on_dismiss=self.handle_dismiss,
        )

    def limpar_erros(self):
        campos = [self.txt_anoFatura, self.txt_mesFatura, self.txt_data, self.dd_banco, self.txt_valorTotal, self.txt_parcela, self.dd_cat, self.dd_user, self.txt_desc]
        
        for campo in campos:
            campo.error_text = None

    def limpar_bs(self, e):
        self.txt_data.value = None
        self.txt_desc.value = None
        self.txt_parcela.value = None
        self.txt_valorTotal.value = None
        self.dd_user.key = 'limpar'
        self.dd_user.value = None
        self.dd_banco.key = 'limpar'
        self.dd_banco.value = None
        self.dd_cat.key = 'limpar'
        self.dd_cat.value = None
        self.txt_mesFatura.value = None
        self.txt_anoFatura.value = None
        self.linha_cadastro.visible = True
        self.linha_confirmacao.visible = False
        self.limpar_erros()
        self.page.update()

    def __open_calendar(self, e):
        self.txt_valorTotal.focus()
        self.page.open(self.calendar)

    def __on_change_calendar(self, e):
        self.txt_data.value = e.control.value.strftime('%d/%m/%Y')
        self.txt_data.data = e.control.value
        self.page.update()

    def __on_dismiss_calendar(self, e):
        self.txt_data.value = None
        self.txt_data.data = None
        self.page.update()

    def abrir_confirmacao(self, e):
        self.linha_cadastro.visible = False
        self.linha_confirmacao.visible = True
        self.page.update()
    
    def cancelar_confirmacao(self, e):
        self.linha_cadastro.visible = True
        self.linha_confirmacao.visible = False
        self.page.update()

    def handle_dismiss(self, e):
        self.linha_cadastro.visible = True
        self.linha_confirmacao.visible = False
    
    def verificar_erro_campos(self) -> bool:
        error_found = False
        msg_erro_vazio = "Todos os campos são obrigatórios."
        campos = [self.txt_anoFatura, self.txt_mesFatura, self.txt_data, self.dd_banco, self.txt_valorTotal, self.txt_parcela, self.dd_cat, self.dd_user, self.txt_desc]
        
        for campo in campos:
            campo.error_text = None
        
        try:
            if int(self.txt_anoFatura.value) < 2022 or int(self.txt_anoFatura.value) > 2035:
                error_found = True
                self.txt_anoFatura.error_text = 'O ano da fatura deve ser entre 2022 e 2035'
            
            if 1 > int(self.txt_mesFatura.value) or 12 < int(self.txt_mesFatura.value):
                error_found = True
                self.txt_mesFatura.error_text = 'O mes da fatura deve ser entre 01 e 12'
            
            if float(self.txt_valorTotal.value.replace(',', '.')) == 0:
                error_found = True
                self.txt_valorTotal.error_text = 'O valor total da compra precisa ser diferente de 0.'
            
            if int(self.txt_parcela.value) < 1:
                error_found = True
                self.txt_parcela.error_text = 'O número de parcelas deve ser maior que 0.'
        except Exception as e:
            error_found = True

        for campo in campos:
            if not campo.value:
                error_found = True
                campo.error_text = msg_erro_vazio

        self.page.update()

        return error_found
    
    def confirmar_cadastro(self, e):
        if not self.verificar_erro_campos():
            hash_str = str(uuid.uuid4())
            parcelas = int(self.txt_parcela.value)
            valor_total = float(self.txt_valorTotal.value.replace(',', '.'))
            valor_parcela = valor_total / parcelas
            fatura_inicial = [f.id for f in self.faturas if f.mes == int(self.txt_mesFatura.value) and f.ano == int(self.txt_anoFatura.value)][0]

            for p in range(parcelas):
                if int(self.dd_user.value) == 3:
                    for i in range(2):
                        self.db.add_compra(user_id=i+1, banco_id=self.dd_banco.value, fatura_id=fatura_inicial+p, categoria_id=self.dd_cat.value, descricao=self.txt_desc.value, valor_total=valor_total, valor_parcela=valor_parcela/2, parcela=f'{p*2+1+i}/{parcelas*2}', data_compra=self.txt_data.data, hash_compra=hash_str)
                else:
                    self.db.add_compra(user_id=int(self.dd_user.value), banco_id=self.dd_banco.value, fatura_id=fatura_inicial+p, categoria_id=self.dd_cat.value, descricao=self.txt_desc.value, valor_total=valor_total, valor_parcela=valor_parcela, parcela=f'{p+1}/{parcelas}', data_compra=self.txt_data.data, hash_compra=hash_str)

            self.bs.open = False
            self.page.update()
            self.page.open(ft.SnackBar(ft.Text('Compra cadastrada com sucesso!')))
    

class MyBsNovaConta:
    def __init__(self, page: ft.Page, db: Database, fatura_id: int, carregar_pagina: Callable):
        self.page = page
        self.db = db
        self.fatura_id = fatura_id
        self.carregar_pagina = carregar_pagina

        self.title = ft.Text('Nova Conta', size=20, weight='bold')

        self.txt_desc = ft.TextField(label='Descrição',)
        self.check_unico = ft.Checkbox(label='Pagamento Único', value=True, on_change=self.handle_change_unico)
        self.check_mensal = ft.Checkbox(label='Pagamento Mensal', on_change=self.handle_change_mensal)
        self.check_anual = ft.Checkbox(label='Pagamento Anual', on_change=self.handle_change_anual)
        self.txt_mes = ft.TextField(label='Mês do Pagamento', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter(), visible=False)

        self.btn_limpar = ft.TextButton('Limpar', on_click=self.limpar)
        self.btn_confirma = ft.ElevatedButton('Cadastrar', bgcolor=ft.Colors.BLUE_900, color='white', on_click=self.abrir_confirmacao)

        self.linha_registro = ft.ResponsiveRow(
            visible=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Container(
                    col={'xs': 6, 'md': 4},
                    content=self.btn_limpar
                ),
                ft.Container(
                    col={'xs': 6, 'md': 4},
                    content=self.btn_confirma
                ),
            ]
        )

        self.txt_pos_confirma = ft.Text('Voce confirma o cadastro dessa compra?', col={'xs': 12})
        self.btn_pos_cancela = ft.ElevatedButton('Cancelar', bgcolor=ft.Colors.RED_900, color='white', elevation=4, col={'xs': 6, 'md': 6}, on_click=self.cancelar_confirmacao)
        self.btn_pos_confirma = ft.ElevatedButton('Confirmar', bgcolor=ft.Colors.BLUE_900, color='white', elevation=4, col={'xs': 6, 'md': 6}, on_click=self.cadastrar_conta)
        self.linha_confirmacao = ft.ResponsiveRow(
            visible=False,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.txt_pos_confirma,
                self.btn_pos_cancela,
                self.btn_pos_confirma,
                ft.Divider(height=10, color='transparent')
            ]
        )

        self.bs = ft.BottomSheet(
            on_dismiss=self.handle_dismiss,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        padding=20,
                        content=ft.Column(
                            tight=True,
                            controls=[
                                self.title,
                                ft.ResponsiveRow(
                                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                                    controls=[
                                        ft.Container(content=self.check_unico, col={'xs': 12, 'md': 4},),
                                        ft.Container(content=self.check_mensal, col={'xs': 12, 'md': 4},),
                                        ft.Container(content=self.check_anual, col={'xs': 12, 'md': 4},),
                                    ]
                                ),
                                ft.ResponsiveRow(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        ft.Container(
                                            col={'xs': 12, 'md': 6},
                                            content=self.txt_mes
                                        ),
                                    ]
                                ),
                                self.txt_desc,
                                self.linha_registro,
                                self.linha_confirmacao
                            ]
                        )
                    )
                ]
            )
        )

        self.page.overlay.append(self.bs)

    def limpar(self, e):
        self.txt_desc.value = None
        self.txt_desc.error_text = None
        self.check_anual.value = False
        self.check_mensal.value = False
        self.check_unico.value = True
        self.txt_mes.value = None
        self.txt_mes.visible = False
        self.txt_mes.error_text = None
        self.page.update()

    def handle_dismiss(self, e):
        self.limpar(None)
    
    def handle_change_mensal(self, e):
        if self.check_mensal.value:
            self.check_unico.value = False
            self.check_anual.value = False
            self.txt_mes.value = None
            self.txt_mes.visible = False
        else:
            self.check_unico.value = True
        self.page.update()

    def handle_change_anual(self, e):
        if self.check_anual.value:
            self.check_unico.value = False
            self.check_mensal.value = False
            self.txt_mes.visible = True
        else:
            self.txt_mes.value = None
            self.txt_mes.visible = False
            self.check_unico.value = True
        
        self.page.update()
    
    def handle_change_unico(self, e):
        if self.check_unico.value:
            self.check_mensal.value = False
            self.check_anual.value = False
            self.txt_mes.value = None
            self.txt_mes.visible = False
        else:
            self.check_unico.value = True
        self.page.update()
    
    def verificar_erro_campos(self) -> bool:
        error_found = False

        if self.check_anual.value and not self.txt_mes.value:
            self.txt_mes.error_text = 'Um valor de 1 a 12 precisa ser inserido.'
            error_found = True
        else:
            self.txt_mes.error_text = None

        if self.txt_mes.value:
            mes = int(self.txt_mes.value)
            if mes < 1 or mes > 12:
                self.txt_mes.error_text = 'O valor "mes" precisa estar entre 1 e 12.'
                error_found = True
            else:
                self.txt_mes.error_text = None

        
        if not self.txt_desc.value:
            self.txt_desc.error_text = 'Esse campo é obrigatório.'
            error_found = True
        else:
            self.txt_desc.error_text = None
        
        self.page.update()
        return error_found
        
    
    def abrir_confirmacao(self, e):
        if not self.verificar_erro_campos():
            self.linha_registro.visible = False
            self.linha_confirmacao.visible = True
            self.page.update()
    
    def cancelar_confirmacao(self, e):
        self.linha_registro.visible = True
        self.linha_confirmacao.visible = False
        self.page.update()
    
    def cadastrar_conta(self, e):
        if self.check_unico.value:
            conta = self.db.get_contas_desc(self.txt_desc.value)
            if not conta:
                conta = self.db.add_conta(self.txt_desc.value, False, 0).data[0]
                conta = Conta.from_json(conta)
            if conta:
                pagamento = self.db.add_pagamento(self.fatura_id, conta.id, 0, False)
        elif self.check_mensal.value:
            conta = self.db.add_conta(self.txt_desc.value, True, 0)
        else:
            conta = self.db.add_conta(self.txt_desc.value, False, int(self.txt_mes.value))
        self.cancelar_confirmacao(None)
        self.bs.open = False
        self.page.update()
        self.carregar_pagina()
        self.page.open(ft.SnackBar(ft.Text(f'Compra "{self.txt_desc.value}" Cadastrada com Sucesso')))