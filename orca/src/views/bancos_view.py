import flet as ft
from database import Database
from .aux import MyAppBar

def bancos_view(page: ft.Page, db: Database):
    
    bancos = db.get_bancos()

    return ft.View(
        route='/bancos',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text('Pagina dos Bancos', weight='bold')
                ] + [ft.Text(banco.nome) for banco in bancos])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
