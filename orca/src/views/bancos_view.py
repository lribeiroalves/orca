import flet as ft
from database import Database
from models import Banco
from .auxiliar import MyAppBar

def bancos_view(page: ft.Page, db: Database):
    
    saldos = db.get_saldos(last=True)
    total_saldos = sum(s.saldo for s in saldos)

    def recarregar_pagina(e):
        page.views.pop()
        page.views.append(bancos_view(page, db))
        page.update()

    # Formulario de Criacao de um Novo Banco
    # Campos
    nome_banco = ft.TextField(label='Nome do Banco')
    saldo_inicial = ft.TextField(label='Saldo', prefix_text='R$ ', input_filter=ft.InputFilter(allow=True, regex_string=r'[0-9.,]', replacement_string=''), keyboard_type=ft.KeyboardType.NUMBER)
    # Funcao para fechar o pop up
    def fechar_popup_banco(e):
        nome_banco.value = ''
        saldo_inicial.value = ''
        popup_banco.open = False
        page.update()
    def fechar_popup_saldo(e):
        nome_banco.value = ''
        nome_banco.disabled = False
        saldo_inicial.value = ''
        popup_saldo.open = False
        page.update()
    # Funcao para Acao do Formulario
    def verifica_campos():
        if not nome_banco.value:
            nome_banco.error_text = 'Por favor, preencha todos os campos'
            page.update()
            return False
        elif not saldo_inicial.value:
            saldo_inicial.error_text = 'Por favor, preencha todos os campos'
            page.update()
            return False
        else:
            return True

    def salvar_novo_banco(e):
        if verifica_campos():
            novo_banco = db.add_banco(nome_banco.value)
            novo_saldo = db.add_saldo(novo_banco.data[0].get('id'), float(saldo_inicial.value))
            fechar_popup_banco(None)
            recarregar_pagina(None)

    def salvar_novo_saldo(e):
        if verifica_campos():
            try:
                banco_id = db.client.table('bancos').select('id').eq('nome', nome_banco.value).execute().data[0].get('id')
                if banco_id:
                    saldo_formatado = ''.join(c for c in saldo_inicial.value if c.isdigit() or c == '.' or c == ',')
                    novo_saldo = db.add_saldo(banco_id=banco_id, saldo=saldo_formatado)
                    fechar_popup_saldo(None)
                    recarregar_pagina(None)
                else:
                    raise Exception('Nao foi possivel encontrar esse Banco.')
            except Exception as e:
                print(f'Ocorreu o erro: {e}, por favor, tente novamente.')
    # Criacao do pop up
    popup_banco = ft.BottomSheet(
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text('Novo Banco', size=20, weight='bold'),
                nome_banco,
                saldo_inicial,
                ft.Row([ft.TextButton('Cancelar', on_click=fechar_popup_banco), ft.ElevatedButton('Salvar', on_click=salvar_novo_banco, bgcolor=ft.Colors.BLUE_900, color='white')], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], tight=True)
        )
    )
    popup_saldo = ft.BottomSheet(
        ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text('Atualizar Saldo', size=20, weight='bold'),
                nome_banco,
                saldo_inicial,
                ft.Row([ft.TextButton('Cancelar', on_click=fechar_popup_saldo), ft.ElevatedButton('Salvar', on_click=salvar_novo_saldo, bgcolor=ft.Colors.BLUE_900, color='white')], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ], tight=True)
        )
    )
    # Funcao para abrir formulario
    def abrir_popup_banco(e):
        page.bottom_sheet = popup_banco
        popup_banco.open = True
        page.update()
    def abrir_popup_saldo(text: str):
        page.bottom_sheet = popup_saldo
        nome_banco.value = text
        nome_banco.disabled = True
        popup_saldo.open = True
        page.update()
    # Adicionando o popup a colecao de overview da pagina
    page.overlay.append(popup_banco)
    page.overlay.append(popup_saldo)

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
                    on_click=lambda _: abrir_popup_saldo(saldo.banco_nome)
                ), padding=10,
            ), elevation=2
        )
    
    card_total = ft.ResponsiveRow(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            ft.Container(
                col={'xs': 6, 'sm': 6, 'md': 3, 'lg': 1},
                content=ft.FloatingActionButton(
                    text='Novo Banco',
                    icon=ft.Icons.ADD,
                    on_click=abrir_popup_banco,
                    bgcolor='blue'
                )
            ),

            ft.Container(
                col={'xs': 12, 'sm': 6, 'md': 6, 'lg': 6},
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
            ),
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
