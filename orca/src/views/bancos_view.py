import flet as ft
from database import Database
from models import Banco
from .aux import MyAppBar

def bancos_view(page: ft.Page, db: Database):
    
    saldos = db.get_saldos(last=True)
    total_saldos = sum(s.saldo for s in saldos)

    def formatar_br(valor):
        return f'R$ {valor:,.2f}'.replace(',','X').replace('.', ',').replace('X', '.')

    def criar_card(saldo):
        return ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.Icon(ft.Icons.ACCOUNT_BALANCE, color=ft.Colors.BLUE_900, size=30),
                    title=ft.Text(saldo.banco_nome, weight='bold', size=18),
                    # subtitle=ft.Text('Saldo Atual', size=12, color='grey'),
                    trailing=ft.Text(
                        formatar_br(saldo.saldo),
                        size=18,
                        weight='bold',
                        color=ft.Colors.BLUE_900
                    ),
                    on_click=lambda _: print(f'clicou no banco: {saldo.banco_nome}'),
                ), padding=10,
            ), elevation=2
        )
    
    card_total = ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.END,
        controls=[
            ft.Container(
                col={'xs': 10, 'sm': 6, 'md': 6},
                content=ft.Card(
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.SUMMARIZE, color=ft.Colors.BLUE_900, size=30),
                        title=ft.Text('Total', weight='bold', size=16),
                        trailing=ft.Text(
                            formatar_br(total_saldos),
                            size=18,
                            weight='bold',
                            color=ft.Colors.BLUE_900
                        )
                    ), elevation=4
                )
            )
        ]
    )

    return ft.View(
        route='/bancos',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text('Minhas Contas', weight='bold', size=28),
                    ft.Divider(height=10, color='transparent'),
                    card_total,
                    ft.Divider(height=20, color='grey', thickness=1),
                    ft.Column(
                        controls=[criar_card(s) for s in saldos],
                        spacing=10
                    ),
                ], expand=True)
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
