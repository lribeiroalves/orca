import flet as ft

def HomeView(page: ft.Page):
    # Função auxiliar para não repetir código dos botões
    def criar_botao_menu(titulo, icone, cor, rota):
        return ft.Container(
            content=ft.Column([
                ft.Icon(name=icone, size=40, color=cor),
                ft.Text(titulo, size=16, weight="bold"),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GRAY_100,
            border_radius=15,
            padding=20,
            on_click=lambda _: page.go(rota), # Navega para a rota ao clicar
            ink=True, # Efeito visual de "toque"
            col={"sm": 6, "md": 4}, # 2 colunas no celular, 3 no tablet
        )

    # Retornamos a View que o main.py vai carregar
    return ft.View(
        "/", # Rota raiz
        controls=[
            ft.AppBar(
                title=ft.Text("ORCA - Gestão Financeira"),
                bgcolor=ft.Colors.BLUE_GREY_900,
                color="white",
                center_title=True
            ),
            ft.Container(
                padding=30,
                content=ft.Column([
                    ft.Text("Bem-vindo de volta!", size=24, weight="bold"),
                    ft.Text("O que deseja gerenciar agora?", color="grey"),
                    ft.Divider(height=20, color="transparent"),
                    
                    # Grade de botões
                    ft.ResponsiveRow([
                        criar_botao_menu("Bancos", ft.Icons.ACCOUNT_BALANCE, "blue", "/bancos"),
                        criar_botao_menu("Contas", ft.Icons.MONETIZATION_ON, "red", "/contas"),
                        criar_botao_menu("Patrimônio", ft.Icons.PIE_CHART, "green", "/patrimonio"),
                        criar_botao_menu("Ajustes", ft.Icons.SETTINGS, "grey", "/config"),
                    ], spacing=20, run_spacing=20),
                ])
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
