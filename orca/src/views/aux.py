import flet as ft


class MyButton(ft.ElevatedButton):
    def __init__(self, text: str, page: ft.Page, route: str):
        super().__init__()
        self.bgcolor = ft.Colors.BLACK38
        self.color = ft.Colors.WHITE
        self.text = text
        self.on_click = lambda _: page.go(route)


class MyAppBar(ft.AppBar):
    def __init__(self, text: str, page: ft.Page):
        super().__init__()
        self.leading = ft.Icon(ft.Icons.ATTACH_MONEY_ROUNDED)
        self.leading_width = 50
        self.title = ft.Text(text, size=16)
        self.center_title = False
        self.bgcolor = ft.Colors.BLACK87
        self.color = ft.Colors.WHITE
        self.actions = [
            ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.on_view_pop(None)),
            ft.IconButton(ft.Icons.HOME_OUTLINED, on_click=lambda _: page.go('/')),
            ft.IconButton(ft.Icons.PLAY_CIRCLE, on_click=lambda _: print(page.views))
        ]


class MyWarnings:
    # Banner para ser exibido quando houver erro de conexao com o Supabase
    banner_conexao = None

    def __init__(self):
        raise SyntaxError("Esta classe não deve ser instanciada. Use os métodos diretamente.")

    @classmethod
    def abrir_banner_conexao(cls, page: ft.Page):
        cls.banner_conexao = ft.Banner(
            bgcolor=ft.Colors.AMBER_100,
            leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
            content=ft.Text(
                value='Nao foi possivel se conectar ao Supabase, verifique se o projeto esta pausado.',
                color=ft.Colors.BLACK
            ),
            actions=[
                ft.TextButton(
                    text='OK', style=ft.ButtonStyle(color=ft.Colors.BLUE), on_click=lambda e: cls.fechar_banner_conexao(page)
                ),
            ],
        )
        page.open(cls.banner_conexao)
    
    @classmethod
    def fechar_banner_conexao(cls, page):
        page.close(cls.banner_conexao)