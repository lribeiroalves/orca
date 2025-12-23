import flet as ft
from database import Database
from .aux import MyAppBar

def fatura_view(page: ft.Page, db: Database):
    
    return ft.View(
        route='/fatura',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text('Pagina da Fatura', weight='bold')
                ])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
