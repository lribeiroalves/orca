import flet as ft
from .custom import MyButton, MyAppBar

def home_view(page: ft.Page):
    botao_fatura = MyButton('Fatura', page, '/fatura')
    botao_bancos = MyButton('Bancos', page, '/bancos')
    botao_contas = MyButton('Contas', page, '/contas')
    botao_es = MyButton('Entrada/Saida', page, '/es')

    return ft.View(
        route='/',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Seja bem vindo!", size=24, weight="bold"),
                    ft.Text("O que deseja gerenciar agora?", color="grey"),
                    ft.Divider(height=30, color="transparent"),
                    
                    ft.ResponsiveRow([
                        ft.Container(col={'xs': 12, 'sm': 4}, content=botao_fatura),
                        ft.Container(col={'xs': 12, 'sm': 4}, content=botao_bancos),
                        ft.Container(col={'xs': 12, 'sm': 4}, content=botao_contas),
                        ft.Container(col={'xs': 12, 'sm': 4}, content=botao_es),
                    ], spacing=20, run_spacing=20),
                ])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
