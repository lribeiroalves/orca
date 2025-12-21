import flet as ft
from database import Database


db = Database()

def main(page: ft.Page):
    page.title = 'teste'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    bancos = db.get_bancos()

    textos = [ft.TextField(value=banco.nome, text_align=ft.TextAlign.CENTER, width=350) for banco in bancos]

    page.add(
        ft.Row(
            [textos[0]],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [textos[1]],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

ft.app(main)