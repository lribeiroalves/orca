import flet as ft
from database import Database
from views import HomeView

def main(page: ft.Page):
    page.title = "Orca App"
    db = Database()

    def route_change(route):
        page.views.clear()
        
        # Se a rota for a inicial
        if page.route == "/":
            page.views.append(HomeView(page))
        
        # Outras rotas
        elif page.route == "/bancos":
            # Aqui você chamaria a BancosView(page, db)
            pass
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)
