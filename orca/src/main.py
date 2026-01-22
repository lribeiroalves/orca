import flet as ft
from database import Database
from views import *
import os
from dotenv import load_dotenv

def verificar_versao(page: ft.Page, db: Database) -> bool:
    load_dotenv()
    versao_atual = os.getenv('VERSION')
    if versao_atual == db.carregar_versao():
        return True
    else:
        container_erro = ft.Column(
            width=page.width,
            height=page.height,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    padding=30,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Seu aplicativo precisa ser atualizado, entre em contato com o desenvolvedor.', size=20, weight='bold')
                        ]
                    )
                )
            ]
        )
        page.add(container_erro)
        page.update()
        return False

def main(page: ft.Page):
    db = Database()
    page.title = "Orca App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("pt", "BR"),
            ft.Locale("en", "US"),
        ],
        current_locale=ft.Locale("pt", "BR"),
    )
    if not verificar_versao(page, db):
        return
    possible_routes = [
        '/',
        '/bancos',
        '/fatura',
        '/contas',
        '/es',
        '/dash',
    ]
    block = True

    def liberar_acesso(route):
        nonlocal block
        block = False
        carregar_pagina(route)

    def carregar_pagina(route):
        match route:
            case '/':
                page.views.append(home_view(page, db))
            case '/bancos':
                page.views.append(bancos_view(page, db))
            case '/contas':
                page.views.append(contas_view(page, db))
            case '/fatura':
                page.views.append(fatura_view(page, db))
            case '/es':
                page.views.append(es_view(page, db))
            case '/dash':
                page.views.append(bancos_view(page, db))
        # print(f'block: {block}, route: {page.route}, views: {len(page.views)}')
        page.update()

    def route_change(route): 
        nonlocal block      
        # Se a rota for a inicial
        if page.route in possible_routes:
            if block:
                page.views.append(login_view(page, db, lambda r=page.route: liberar_acesso(r)))
            else:
                carregar_pagina(page.route)
            
        page.update() 

    def view_pop(view):
        if len(page.views) > 3:
            page.views.pop()
            top_view = page.views[-1]
            if top_view.route == '/login':
                page.views.pop()
                top_view = page.views[-1]
            page.views.pop()
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main, assets_dir='assets')
