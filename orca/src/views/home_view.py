import flet as ft
from .auxiliar import MyButton, MyAppBar, MyWarnings
from database import Database

def home_view(page: ft.Page, db: Database):
    botao_fatura = MyButton('Fatura', page, '/fatura')
    botao_bancos = MyButton('Bancos', page, '/bancos')
    botao_contas = MyButton('Contas', page, '/contas')
    botao_es = MyButton('Entrada/Saida', page, '/es')
    botao_dash = MyButton('DashBoard', page, '/dash')
    area_erro = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def recarregar_pagina(e):
        page.views.pop()
        page.views.append(home_view(page, db))
        page.update()

    def testar_conexao():
        try:
            r = db.get_bancos()
            if r == []:
                raise Exception()             
        except:
            MyWarnings.abrir_banner_conexao(page)
            botao_bancos.disabled = True
            botao_contas.disabled = True
            botao_es.disabled = True
            botao_fatura.disabled = True
            botao_dash.disabled = True
            area_erro.controls = [
                ft.Divider(height=30, color='transparent'),
                ft.ElevatedButton('Tentar Conexao', icon=ft.Icons.REFRESH, on_click=lambda e: recarregar_pagina(e))
            ]
    
    testar_conexao()

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
                        ft.Container(col={'xs': 12, 'sm': 4}, content=botao_dash),
                    ], spacing=20, run_spacing=20),
                    
                    area_erro
                ])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
