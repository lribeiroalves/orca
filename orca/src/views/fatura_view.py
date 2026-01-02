import flet as ft
from database import Database
from models import Compra
from .aux import MyAppBar

def fatura_view(page: ft.Page, db: Database):

    faturas = db.get_faturas()
    bancos = [b for b in db.get_bancos() if b.cartao]
    anos = [ft.DropdownOption(key=str(f.ano), content=ft.Text(f.ano)) for f in faturas]
    meses = []

    card_total = ft.Container(visible=False)
    def criar_card(compras: list[Compra]):
        status = 'PAGA' if compras[0].fatura_paga else 'EM ABERTO'
        totais = {'total': 0.0}
        for c in compras:
            valor = c.valor_parcela
            user = c.user_nome

            totais['total'] += valor

            if user in totais:
                totais[user] += valor
            else:
                totais[user] = valor

        return ft.Container(
            visible=True,
            alignment=ft.alignment.center,
            col={'xs': 12, 'sm': 12, 'md': 12, 'lg': 12},
            content=ft.Card(
                content=ft.Container(
                    padding=20,
                    content=ft.ResponsiveRow(
                        controls=[
                            ft.Card(
                                col={'md': 5},
                                elevation=2,
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MONEY, color=ft.Colors.BLUE_900, size=30),
                                    title=ft.Text('Status', weight='bold', size=16),
                                    trailing=ft.Text(
                                        status,
                                        size=18,
                                        weight='bold',
                                        color=ft.Colors.BLUE_900
                                    )
                                )
                            ),
                            ft.Card(
                                col={'md': 5},
                                elevation=2,
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MONEY, color=ft.Colors.BLUE_900, size=30),
                                    title=ft.Text('Total', weight='bold', size=16),
                                    trailing=ft.Text(
                                        f'R$ {totais["total"]:.2f}',
                                        size=18,
                                        weight='bold',
                                        color=ft.Colors.BLUE_900
                                    )
                                )
                            ),
                            ft.Card(
                                col={'md': 5},
                                elevation=2,
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MONEY, color=ft.Colors.BLUE_900, size=30),
                                    title=ft.Text('Total Lucas', weight='bold', size=16),
                                    trailing=ft.Text(
                                        f'R$ {totais["Lucas"]:.2f}',
                                        size=18,
                                        weight='bold',
                                        color=ft.Colors.BLUE_900
                                    )
                                )
                            ),
                            ft.Card(
                                col={'md': 5},
                                elevation=2,
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.MONEY, color=ft.Colors.BLUE_900, size=30),
                                    title=ft.Text('Total Selma', weight='bold', size=16),
                                    trailing=ft.Text(
                                        f'R$ {totais["Selma"]:.2f}',
                                        size=18,
                                        weight='bold',
                                        color=ft.Colors.BLUE_900
                                    )
                                )
                            ),
                        ]
                    )
                ), elevation=4
            )
        )

    tabela = ft.DataTable(
        visible=False,
        columns=[
            ft.DataColumn(ft.Text('User')),
            ft.DataColumn(ft.Text('Data')),
            ft.DataColumn(ft.Text('Categoria')),
            ft.DataColumn(ft.Text('Descrição')),
            ft.DataColumn(ft.Text('Valor Total'), numeric=True),
            ft.DataColumn(ft.Text('Valor Parcela'), numeric=True),
            ft.DataColumn(ft.Text('Parcela')),
        ],
        rows=[]
    )

    tabela_compras = ft.Row(
        scroll=ft.ScrollMode.AUTO,
        controls=[tabela]
    )

    # Botao OK
    def filtrar_compras(e):
        compras = db.get_compras_filter(dd_ano.value, dd_mes.value, dd_banco.value)
        card_total.content = criar_card(compras)
        card_total.visible = True
        tabela.rows.clear()
        tabela.rows.extend([
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(c.user_nome)),
                    ft.DataCell(ft.Text(c.data_compra.strftime('%d/%m/%Y'))),
                    ft.DataCell(ft.Text(c.categoria_nome)),
                    ft.DataCell(ft.Text(c.descricao)),
                    ft.DataCell(ft.Text(f'R$ {c.valor_total:.2f}'.replace('.', ','))),
                    ft.DataCell(ft.Text(f'R$ {c.valor_parcela:.2f}'.replace('.', ','))),
                    ft.DataCell(ft.Text(c.parcela)),
                ]
            ) for c in compras
        ])
        tabela.visible=True
        page.update()

    btn_ok = ft.ElevatedButton('OK', on_click=filtrar_compras, bgcolor='grey', color='white', col={'xs': 6, 'sm': 6, 'md': 2, 'lg': 3}, disabled=True)

    def habilitar_btn_ok():
        if dd_ano.value and dd_mes.value and dd_banco.value:
            btn_ok.disabled = False
            btn_ok.bgcolor = ft.Colors.BLUE_900
        else:
            btn_ok.disabled = True
            btn_ok.bgcolor = 'grey'
    
    # Botao Limpar
    def limpar_tela(e):
        dd_ano.key = 'limpar'
        dd_ano.value = None
        dd_mes.key = 'limpar'
        dd_mes.value = None
        dd_banco.key = 'limpar'
        dd_banco.value = None
        tabela.rows.clear()
        tabela.visible=False
        habilitar_btn_ok()
        card_total.visible=False
        card_total.content = None
        page.update()
    
    btn_limpar = ft.ElevatedButton('Limpar', on_click=limpar_tela, col={'xs': 6, 'sm': 6, 'md': 2, 'lg': 3})

    # Dropdown
    def change_ano(e):
        # Reset dos outros dropdowns
        meses = [f for f in faturas if f.ano == float(dd_ano.value)]
        dd_mes.value = None
        dd_mes.key = 'reset do dd_mes'
        dd_banco.value = None
        dd_banco.key = 'reset do dd_ano'
        dd_mes.options.clear()
        dd_mes.options.extend([ft.DropdownOption(key=str(f.mes), text=f.mes_str.upper(), content=ft.Text(f.mes_str.upper())) for f in meses])
        # habilitar btn_ok
        habilitar_btn_ok()
        page.update()
    
    def change_mes(e):
        dd_banco.value = None
        dd_banco.key = 'reset do dd_ano'
        habilitar_btn_ok()
        page.update()
    
    def change_banco(e):
        habilitar_btn_ok()
        page.update()

    dd_ano = ft.Dropdown(
        border = ft.InputBorder.UNDERLINE,
        enable_filter = False,
        editable = False,
        leading_icon = ft.Icons.CALENDAR_MONTH,
        label = 'Ano',
        options = anos,
        on_change = change_ano,
        expand = True,
        width = 300
    )

    dd_mes = ft.Dropdown(
        border = ft.InputBorder.UNDERLINE,
        enable_filter = False,
        editable = False,
        leading_icon = ft.Icons.CALENDAR_MONTH,
        label = 'Mes',
        options = [],
        on_change = change_mes,
        expand = True,
        width = 300
    )

    dd_banco = ft.Dropdown(
        border = ft.InputBorder.UNDERLINE,
        enable_filter = False,
        editable = False,
        leading_icon = ft.Icons.CALENDAR_MONTH,
        label = 'Banco',
        options = [ft.DropdownOption(key=str(b.id), text=b.nome, content=ft.Text(b.nome)) for b in bancos],
        on_change = change_banco,
        expand = True,
        width = 300
    )
    
    return ft.View(
        route='/fatura',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text('Minhas Faturas', weight='bold', size=28),
                    ft.Divider(height=10, color='transparent'),
                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            ft.Container(
                                col={'xs': 10, 'sm': 10, 'md': 4, 'lg': 2},
                                content=dd_ano
                            ),
                            ft.Container(
                                col={'xs': 10, 'sm': 10, 'md': 4, 'lg': 2},
                                content=dd_mes
                            ),
                            ft.Container(
                                col={'xs': 10, 'sm': 10, 'md': 4, 'lg': 2},
                                content=dd_banco
                            ),
                        ]
                    ),
                    ft.Divider(height=10, color='transparent'),
                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            btn_limpar,
                            btn_ok,
                        ],
                    ),
                    ft.Divider(height=20, color='grey', thickness=1),
                    card_total,
                    ft.Container(
                        content=tabela_compras,
                        alignment=ft.alignment.center,
                        width=float('inf')
                    ),
                    ft.ElevatedButton('Popular Compras', on_click=lambda _: db.popular_compras(), bgcolor=ft.Colors.RED_900)
                ])
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
