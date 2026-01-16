import flet as ft
from database import Database
from models import Compra
from .auxiliar import MyAppBar, MyPopup, MyBsAddCompra

def fatura_view(page: ft.Page, db: Database):

    # Coleta de dados
    ######################################################################################################################
    faturas = db.get_faturas()
    bancos = [b for b in db.get_bancos() if b.cartao]
    categorias = db.get_categorias()
    anos_unicos = sorted(list(set(f.ano for f in faturas)))
    anos = [ft.DropdownOption(key=str(ano), content=ft.Text(ano)) for ano in anos_unicos]
    meses = []
    compras = []

    # Card de Totais
    ######################################################################################################################
    titulo_fatura = ft.Text(value='', size=30, weight='bold')
    card_total = ft.Container(visible=False)
    text_status = ft.Text(
        value='',
        size=18,
        weight='bold',
        color=ft.Colors.BLUE_900
    )
    def criar_card(compras: list[Compra]):
        text_status.value = 'PAGA' if compras[0].fatura_paga else 'EM ABERTO'
        totais = {'total': 0.0, 'Lucas': 0.0, 'Selma': 0.0}
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
                                    trailing=text_status
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


    # Tabela de Faturas
    ######################################################################################################################
    def executar_ordenacao(index: int, ascending: bool):
        nonlocal compras

        if index == 0:
            compras.sort(key=lambda x: x.user_id, reverse=not ascending)
        if index == 1:
            compras.sort(key=lambda x: x.data_compra, reverse=not ascending)
        
        carregar_items_tabela(compras)
    
    def ordernar_coluna(e):
        tabela.sort_column_index = e.column_index
        tabela.sort_ascending = e.ascending
        executar_ordenacao(e.column_index, e.ascending)
        page.update()
    
    tabela = ft.DataTable(
        visible=False,
        show_checkbox_column=False,
        sort_column_index=1,
        sort_ascending=False,
        columns=[
            ft.DataColumn(ft.Text('User'), on_sort=ordernar_coluna),
            ft.DataColumn(ft.Text('Data'), on_sort=ordernar_coluna),
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


    # Filtros Superiores
    ######################################################################################################################
    # Botao OK
    def carregar_items_tabela(compras: list[Compra]):
        tabela.rows.clear()
        tabela.rows.extend([
            ft.DataRow(
                data=c.hash_compra,
                color= ft.Colors.with_opacity(0.3, ft.Colors.GREY) if i % 2 != 0 else ft.Colors.with_opacity(0.1, ft.Colors.GREY),
                selected=False,
                on_select_changed=lambda e, compra=c: abrir_popup_compra(e, compra),
                cells=[
                    ft.DataCell(ft.Text(c.user_nome)),
                    ft.DataCell(ft.Text(c.data_compra.strftime('%d/%m/%Y'))),
                    ft.DataCell(ft.Text(c.categoria_nome)),
                    ft.DataCell(ft.Text(c.descricao)),
                    ft.DataCell(ft.Text(f'R$ {c.valor_total:.2f}'.replace('.', ','))),
                    ft.DataCell(ft.Text(f'R$ {c.valor_parcela:.2f}'.replace('.', ','))),
                    ft.DataCell(ft.Text(c.parcela)),
                ]
            ) for i, c in enumerate(compras)
        ])

    def filtrar_compras(e):
        nonlocal compras
        compras = db.get_compras_filter(dd_ano.value, dd_mes.value, dd_banco.value)
        if not compras:
            dd_ano.error_text = 'Não foram encontrados resultados'
            dd_mes.error_text = 'Não foram encontrados resultados'
            dd_banco.error_text = 'Não foram encontrados resultados'
            limpar_tela(None)
            page.update()
            return
        titulo_fatura.value = f'Fatura: {compras[0].fatura_str} \nBanco: {compras[0].banco_nome}'.title()
        titulo_fatura.data = [compras[0].fatura_id, compras[0].fatura_paga]
        titulo_fatura.visible = True
        card_total.content = criar_card(compras)
        card_total.visible = True
        carregar_items_tabela(compras=compras)
        tabela.visible=True
        linha_acao.visible = True
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
        linha_acao.visible = False
        titulo_fatura.visible = False
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
        dd_mes.options.extend([ft.DropdownOption(key=str(f.mes), text=f.mes_str.upper(), content=ft.Text(f.mes_str.upper(), color='blue' if f.fatura_paga else 'red')) for f in meses])
        habilitar_btn_ok()
        dd_ano.error_text = ''
        dd_mes.error_text = ''
        dd_banco.error_text = ''
        page.update()
    
    def change_mes(e):
        dd_banco.value = None
        dd_banco.key = 'reset do dd_ano'
        habilitar_btn_ok()
        dd_ano.error_text = ''
        dd_mes.error_text = ''
        dd_banco.error_text = ''
        page.update()
    
    def change_banco(e):
        habilitar_btn_ok()
        dd_ano.error_text = ''
        dd_mes.error_text = ''
        dd_banco.error_text = ''
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

    # Botoes de Acao
    ######################################################################################################################
    # Cadastrar compra
    nova_compra = ft.ElevatedButton('Cadastrar Nova Compra', bgcolor=ft.Colors.BLUE_700, color='white', on_click=lambda _: (setattr(bs_compra, 'open', True), page.update()), col={'xs': 11, 'sm': 11, 'md': 8, 'lg': 8})
    # Alterar Status de Fatura
    btn_altera_status = ft.ElevatedButton('Alterar Status da Fatura', bgcolor=ft.Colors.BLUE_900, color='white', on_click=lambda _: (setattr(popup_confirma_status, 'open', True), page.update()))

    linha_acao = ft.ResponsiveRow(
        visible=False,
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            # ft.Container(
            #     col={'xs': 12, 'md': 3},
            #     content=nova_compra
            # ),
            ft.Container(
                col={'xs': 12, 'md': 3},
                content=btn_altera_status
            ),
        ]
    )

    #   POPUPS
    ######################################################################################################################

    txt_data = ft.TextField(label='Data da Compra', read_only=True)
    txt_parcela = ft.TextField(label='Parcela', read_only=True)
    txt_valorTotal = ft.TextField(label='Valor Total', read_only=True, prefix_text='R$ ', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(allow=True, regex_string=r'[0-9.,]', replacement_string=''))
    txt_valorParcela = ft.TextField(label='Valor da Parcela', read_only=True, prefix_text='R$ ', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(allow=True, regex_string=r'[0-9.,]', replacement_string=''))
    txt_desc = ft.TextField(label='Descrição', read_only=True)

    tabela_parcelamento = ft.DataTable(
        visible=True,
        show_checkbox_column=False,
        columns=[
            ft.DataColumn(ft.Text('Usuário')),
            ft.DataColumn(ft.Text('Fatura')),
            ft.DataColumn(ft.Text('Parcela')),
        ],
        rows=[]
    )

    popup_compra = ft.BottomSheet(
        ft.Column([
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Container(
                                col={'xs': 8, 'md': 6},
                                content=ft.Text('Visualizar Compra', size=20, weight='bold')
                            ),
                            ft.Container(
                                col={'xs': 4, 'md': 4},
                                content=ft.ElevatedButton(' Excluir ', on_click=lambda _: (setattr(popup_confirma_exclusao, 'open', True), page.update()),bgcolor='red', color='white')
                            ),
                        ]
                    ),
                    ft.Divider(height=15, color='transparent'),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Container(
                                col={'xs':12, 'md': 6},
                                content=txt_data
                            ),
                            ft.Container(
                                col={'xs':12, 'md': 6},
                                content=txt_parcela
                            ),
                            ft.Container(
                                col={'xs':12, 'md': 6},
                                content=txt_valorTotal
                            ),
                            ft.Container(
                                col={'xs':12, 'md': 6},
                                content=txt_valorParcela
                            ),
                        ]
                    ),
                    txt_desc,
                    ft.Text('Parcelamento'),
                    ft.Container(
                        content=tabela_parcelamento,
                        alignment=ft.alignment.center
                    )

                ], tight=True)
            )], scroll=ft.ScrollMode.AUTO
        )  
    )

    def abrir_popup_compra(e, compra: Compra):
        parcelamento = db.get_compras_hash(compra.hash_compra)
        tabela_parcelamento.rows.clear()
        tabela_parcelamento.rows.extend([
            ft.DataRow(
                color= ft.Colors.with_opacity(0.3, ft.Colors.GREY) if i % 2 != 0 else ft.Colors.with_opacity(0.1, ft.Colors.GREY),
                selected=False,
                cells=[
                    ft.DataCell(ft.Text(c.user_nome)),
                    ft.DataCell(ft.Text(c.fatura_str)),
                    ft.DataCell(ft.Text(c.parcela)),
                ]
            ) for i, c in enumerate(parcelamento)
        ])
        txt_data.value = compra.data_compra.strftime('%d/%m/%Y')
        txt_data.data = e.control
        txt_desc.value = compra.descricao
        txt_parcela.value = compra.parcela
        txt_valorTotal.value = f'{compra.valor_total:.2f}'.replace('.', ',')
        txt_valorParcela.value = f'{compra.valor_parcela:.2f}'.replace('.', ',')
        page.bottom_sheet = popup_compra
        popup_compra.data = compra
        popup_compra.open = True
        page.update()

    def confirma_exclusao(e):
        nonlocal compras
        response = db.delete_compra_hash(popup_compra.data.hash_compra)
        compras_removidas = [compra for compra in compras if compra.hash_compra == popup_compra.data.hash_compra]
        for c in compras_removidas:
            compras.remove(c)
        carregar_items_tabela(compras)
        tabela.update()
        popup_confirma_exclusao.open = False
        popup_compra.open = False
        page.update()
        page.open(ft.SnackBar(ft.Text(f'{len(response.data)} linhas excluídas.')))

    popup_confirma_exclusao =  MyPopup('Deseja mesmo excluir essa compra?', confirma_exclusao, page).popup

    def alterar_status(fatura: ft.Text):
        f_id = fatura.data[0]
        f_status = not fatura.data[1]
        update = db.update_fatura(f_id, f_status)
        if update:
            text_status.value = 'PAGA' if f_status else 'EM ABERTO'
            fatura_alterada = next((fatura for fatura in faturas if fatura.id == f_id), None)
            if fatura_alterada:
                fatura_alterada.fatura_paga = f_status
            fatura.data[1] = f_status
            page.update()
        popup_confirma_status.open = False
        page.update()

    popup_confirma_status =  MyPopup('Deseja mesmo alterar o status dessa fatura?', lambda e: alterar_status(titulo_fatura), page).popup

    # CADASTRAR COMPRA
    ######################################################################################################################

    bs_compra = MyBsAddCompra(page, faturas, categorias, bancos, db).bs

    # ADICIONAR POPUPS A PAGINA
    ######################################################################################################################

    page.overlay.append(popup_confirma_exclusao)
    page.overlay.append(popup_confirma_status)
    page.overlay.append(bs_compra)
    page.overlay.append(popup_compra)

    # VIEW
    ######################################################################################################################
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
                    ft.Container(
                        alignment=ft.alignment.center,
                        content=ft.ResponsiveRow(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                btn_limpar,
                                btn_ok,
                                nova_compra,
                            ],
                        )
                    ),
                    ft.Divider(height=20, color='grey', thickness=1),
                    titulo_fatura,
                    card_total,
                    ft.Column(
                        controls=[
                            ft.Divider(height=30, color='transparent'),
                            linha_acao,
                            ft.Divider(height=20, color='transparent', thickness=1),
                        ]
                    ),
                    ft.Container(
                        content=tabela_compras,
                        alignment=ft.alignment.center,
                        width=float('inf')
                    ),
                ])
            )
        ],
        scroll=ft.ScrollMode.AUTO
    )
