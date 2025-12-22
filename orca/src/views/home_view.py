import flet as ft
from .custom import MyButton, MyAppBar

def HomeView(page: ft.Page):
    # Retorna a View que sera carregada

    botao_fatura = MyButton('Fatura')
    botao_bancos = MyButton('Bancos')
    botao_contas = MyButton('Contas')
    botao_es = MyButton('Entrada/Saida')

    return ft.View(
        route="/",
        appbar=MyAppBar('ORCA - Orcamento Familiar'),

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
