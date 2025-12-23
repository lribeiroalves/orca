import flet as ft
from database import Database
from .aux import MyAppBar

def es_view(page: ft.Page, db: Database):
    
    return ft.View(
        route='/es',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text('Pagina dos Registros de Entrada e Saida Mensais', weight='bold')
                ])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
