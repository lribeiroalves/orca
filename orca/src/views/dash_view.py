import flet as ft
from database import Database
from .aux import MyAppBar

def dash_view(page: ft.Page, db: Database):
    
    return ft.View(
        route='/dash',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text('Pagina do DashBoard', weight='bold')
                ])
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
