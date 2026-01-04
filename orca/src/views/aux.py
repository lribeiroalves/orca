import flet as ft
from typing import Callable
from models import Fatura, Categoria, Banco
from datetime import datetime


class MyButton(ft.ElevatedButton):
    def __init__(self, text: str, page: ft.Page, route: str):
        super().__init__()
        self.bgcolor = ft.Colors.BLACK38
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
        self.actions = [
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.on_view_pop(None)),
            ft.IconButton(ft.Icons.HOME_OUTLINED, on_click=lambda _: page.go('/')),
            ft.IconButton(ft.Icons.PLAY_CIRCLE, on_click=lambda _: print(page.views))
        ]


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
    def __init__(self, p: ft.Page, faturas: list[Fatura], categorias: list[Categoria], bancos: list[Banco]):
        self.page = p

        self.title = 'Cadastrar Compra'

        self.txt_data = ft.TextField(label='Data da Compra', read_only=True, on_focus=self.__open_calendar)
        self.calendar = ft.DatePicker(on_change=self.__on_change_calendar, on_dismiss=self.__on_dismiss_calendar, date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY)

        self.txt_parcela = ft.TextField(label='Parcelas', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.NumbersOnlyInputFilter())

        self.reg_str = r"^(|[0-9][0-9]*(,[0-9]{0,2})?)$"
        self.txt_valorTotal = ft.TextField(label='Valor Total', prefix_text='R$ ', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = self.reg_str, allow=True, replacement_string=""))

        self.txt_desc = ft.TextField(label='Descrição')

        self.opt_user = [ft.DropdownOption(key='1', content=ft.Text('Lucas'), text='Lucas'), ft.DropdownOption(key='2', content=ft.Text('Selma'), text='Selma'), ft.DropdownOption(key='3', content=ft.Text('Ambos'), text='Ambos')]
        self.dd_user = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Usuário', options=self.opt_user, expand=True, width=500)

        self.opt_banco = [ft.DropdownOption(key=b.id, content=b.nome, text=b.nome) for b in bancos]
        self.dd_banco = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Banco', options=self.opt_banco, expand=True, width=500)

        self.opt_cat = [ft.DropdownOption(key=c.id, content=c.categoria, text=c.categoria) for c in categorias]
        self.dd_cat = ft.Dropdown(border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Categoria', options=self.opt_cat, expand=True, width=500)

        self.txt_mesFatura = ft.TextField(label='Mês da Fatura', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = r"^[0-9]{0,2}$", allow=True, replacement_string=""), hint_text='Ex: 02', value=datetime.now().strftime('%m'))
        self.txt_anoFatura = ft.TextField(label='Ano da Fatura', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = r"^[0-9]{0,4}$", allow=True, replacement_string=""), hint_text='Ex: 2025', value=datetime.now().strftime('%Y'))

        
        self.txt_valorParcela = ft.TextField(label='Placehoder', read_only=True)

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
                                    content=self.txt_data
                                ),
                                ft.Container(
                                    col={'xs':12, 'md': 6},
                                    content=self.dd_banco
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

                    ], tight=True)
                )], scroll=ft.ScrollMode.AUTO
            )  
        )

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
        self.page.update()

    def __open_calendar(self, e):
        self.txt_parcela.focus()
        self.page.open(self.calendar)

    def __on_change_calendar(self, e):
        self.txt_data.value = e.control.value.strftime('%d/%m/%Y')
        self.txt_data.data = e.control.value.strftime('%Y-%m-%d')
        self.page.update()

    def __on_dismiss_calendar(self, e):
        self.txt_data.value = None
        self.txt_data.data = None
        self.page.update()