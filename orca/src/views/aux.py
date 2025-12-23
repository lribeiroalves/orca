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