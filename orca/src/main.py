import flet as ft
from database import Database
from views import *

def main(page: ft.Page):
    db = Database()
    page.title = "Orca App"
    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale("pt", "BR"),
            ft.Locale("en", "US"),
        ],
        current_locale=ft.Locale("pt", "BR"),
    )

    def liberar_acesso(route):
        page.go(route)

    def route_change(route):        
        # Se a rota for a inicial
        if page.route == "/":
            page.views.append(home_view(page, db))
        
        # Outras rotas
        elif page.route == "/bancos":
            page.views.append(login_view(page, db, lambda r=page.route: liberar_acesso('/bancos-safe')))
        
        elif page.route == '/bancos-safe':
            page.views.append(bancos_view(page, db))
        
        elif page.route == "/fatura":
            page.views.append(fatura_view(page, db))
        
        elif page.route == "/contas":
            page.views.append(contas_view(page, db))
        
        elif page.route == "/es":
            page.views.append(login_view(page, db, lambda r=page.route: liberar_acesso('/es-safe')))
        
        elif page.route == "/es-safe":
            page.views.append(es_view(page, db))
        
        elif page.route == '/dash':
            page.views.append(login_view(page, db, lambda r=page.route: liberar_acesso('/dash-safe')))
        
        elif page.route == '/dash-safe':
            page.views.append(dash_view(page, db))
        
        elif page.route == '/login':
            page.views.append(login_view(page, db, lambda r=route: liberar_acesso('/bancos')))
            
        page.update()

    def view_pop(view):
        if len(page.views) > 2:
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
