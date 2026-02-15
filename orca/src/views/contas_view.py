import flet as ft
from database import Database
from .aux import MyAppBar, MyBsNovaConta
from datetime import datetime
from dotenv import load_dotenv
import os
from models import Pagamento
from functools import partial
import time
import threading

def contas_view(page: ft.Page, db: Database):
    load_dotenv()
    ano_max = int(os.getenv('FATURA_ANO_MAX'))
    ano_min = int(os.getenv('FATURA_ANO_MIN'))
    fatura = []
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    txt_data_ano = ft.TextField(label='Ano', read_only=True, value=datetime.now().strftime('%Y'))
    txt_data_mes = ft.TextField(label='Mes', read_only=True, value=datetime.now().strftime('%m'))
    data_selecionada = ft.Text(f'{meses[int(txt_data_mes.value) - 1]} / {txt_data_ano.value}', size=28, weight='bold')
    linha_exibicao_dados = ft.Column(
        controls=[],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    tabela_pagamentos = ft.DataTable(
        col={'xs': 12, 'md': 9, 'lg': 7},
        visible=False,
        show_checkbox_column=False,
        column_spacing=20,
        columns=[
            ft.DataColumn(ft.Text('Descrição')),
            ft.DataColumn(ft.Text('Valor'), numeric=True),
            ft.DataColumn(ft.Text('Status'))
        ],
        rows=[],
    )
    linha_tabela = ft.ResponsiveRow(
        controls=[tabela_pagamentos],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    lose_focus = True
    def select_all(e):
        nonlocal lose_focus
        if lose_focus:
            time.sleep(0.1)
            e.control.blur()
            time.sleep(0.1)
            e.control.focus()
            e.control.selection_start = 0
            e.control.selection_end = len(str(e.control.value))
            e.control.update()
            lose_focus = False

    text_valor_total = ft.Text(value=None, size=20)
    txt_valor_dialogue = ft.TextField(label='Valor', on_focus=select_all, col={'xs': 12, 'md': 5}, prefix_text='R$ ', keyboard_type=ft.KeyboardType.NUMBER, input_filter=ft.InputFilter(regex_string = r"^(|-|(-?[0-9]+([.,][0-9]{0,2})?))$", allow=True, replacement_string=""))
    opt_status_dialogue = [ft.DropdownOption(key=False, content=ft.Text('PENDENTE'), text='PENDENTE'), ft.DropdownOption(key=True, content=ft.Text('PAGO'), text='PAGO')]
    drop_status_dialogue = ft.Dropdown(col={'xs': 12, 'md': 5}, border=ft.InputBorder.OUTLINE, enable_filter=False, editable=False, label='Status', expand=True, options=opt_status_dialogue)
    title_dialogue = ft.Text('')
    btn_confirma_dialogue = ft.ElevatedButton('     Confirma     ', bgcolor=ft.Colors.BLUE_900, color='white', on_click=lambda _: atualizar_pagamento(title_dialogue.data))
    dialogue = ft.AlertDialog(
        title=title_dialogue,
        content=ft.Column(
            tight=True,
            width=500,
            controls=[
                ft.Divider(height=15, color='transparent'),
                ft.ResponsiveRow(
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        txt_valor_dialogue,         
                        drop_status_dialogue
                    ]
                )
            ]
        ),
        actions=[
            btn_confirma_dialogue
        ]
    )

    def atualizar_pagamento(pagamento: Pagamento):
        try:   
            db.update_pagamento(pagamento.id, float(txt_valor_dialogue.value.replace(',', '.')), drop_status_dialogue.value)
            carregar_data(pagamento.fatura_ano, pagamento.fatura_mes)
            dialogue.open = False
            page.open(ft.SnackBar(ft.Text(f'Pagamento: {pagamento.conta_desc} atualizado com sucesso.')))
        except:
            dialogue.open = False
            page.open(ft.SnackBar(ft.Text(f'Houve um erro')))

    def criar_card(ano:int, mes: int):
        return ft.Container(
        alignment=ft.alignment.center,
        col = {'xs': 12},
        content=ft.Container(
            padding=20,
            content=ft.ResponsiveRow(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Card(
                        col={'xs': 12, 'md':5},
                        elevation=4,
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.ATTACH_MONEY),
                            title=ft.Text('Total', size=16, weight='bold'),
                            trailing=text_valor_total
                        )
                    ),
                    ft.ElevatedButton('    Carregar Pagamentos    ', col={'xs': 12, 'md':4}, bgcolor=ft.Colors.BLUE_900, color='white', on_click=lambda _: carregar_pagamentos(ano, mes))
                ]
            )
        )
    )

    def carregar_data(ano: int, mes: int):
        nonlocal fatura
        txt_data_ano.value = f'{ano:04d}'
        txt_data_mes.value = f'{mes:02d}'
        data_selecionada.value = f'{meses[int(txt_data_mes.value) - 1]} / {txt_data_ano.value}'
        fatura = db.get_faturas_data(mes, ano)[0]
        pagamentos = db.get_pagamentos_date(ano, mes)
        linha_exibicao_dados.controls.clear()
        if not pagamentos:
            tabela_pagamentos.visible = False
            linha_exibicao_dados.controls.extend([
                ft.Text('Nenhum pagamento cadastrado.'),
                ft.ElevatedButton('    Carregar Pagamentos    ', bgcolor=ft.Colors.BLUE_900, color='white', on_click=lambda _: carregar_pagamentos(ano, mes))
            ])
        else:
            text_valor_total.value = f'R$ {sum(p.valor for p in pagamentos):.2f}'.replace('.', ',')
            card_total = criar_card(ano, mes)
            tabela_pagamentos.rows.clear()
            tabela_pagamentos.rows.extend([
                ft.DataRow(
                    data = p.id,
                    color= ft.Colors.with_opacity(0.3, ft.Colors.GREY) if i % 2 != 0 else ft.Colors.with_opacity(0.1, ft.Colors.GREY),
                    selected=False,
                    on_select_changed=lambda e, pagamento = p: abrir_dialogue(pagamento),
                    cells=[
                        ft.DataCell(ft.Text(p.conta_desc)),
                        ft.DataCell(ft.Text(f'R$ {p.valor:.2f}'.replace('.', ','))),
                        ft.DataCell(ft.Text('PAGO' if p.pago else 'PENDENTE'))
                    ]
                ) for i, p in enumerate(pagamentos)
            ])
            tabela_pagamentos.visible = True
            linha_exibicao_dados.controls.extend([
                card_total,
                linha_tabela
            ])
        page.update()

    def voltar_data(e):
        ano = int(txt_data_ano.value)
        mes = int(txt_data_mes.value)
        if mes > 1:
            mes -= 1
            carregar_data(ano, mes)
        elif ano > ano_min:
            mes = 12
            ano -= 1
            carregar_data(ano, mes)

    def avancar_data(e):
        ano = int(txt_data_ano.value)
        mes = int(txt_data_mes.value)
        if mes < 12:
            mes += 1
            carregar_data(ano, mes)
        elif ano < ano_max:
            mes = 1
            ano += 1
            carregar_data(ano, mes)
    
    def carregar_pagamentos(ano: int, mes: int):
        nonlocal fatura
        pagamentos = db.get_pagamentos_date(ano, mes)
        contas = db.get_contas_or(mes)
        if not contas:
            page.open(ft.SnackBar(ft.Text('Nenhum pagamento para ser carregado.')))
            carregar_data(ano, mes)
            return
        ids_pagos = {p.conta_id for p in pagamentos}
        contas_pendentes = [c for c in contas if c.id not in ids_pagos]
        if not contas_pendentes:
            page.open(ft.SnackBar(ft.Text('Todos os pagamentos cadastrados já foram carregados.')))
            return
        for c in contas_pendentes:
            pagamento_cadastrado = db.add_pagamento(fatura_id=fatura.id, conta_id=c.id, valor=0, pago=False)
        carregar_data(ano, mes)
        page.open(ft.SnackBar(ft.Text('Pagamentos carregados com sucesso.')))
    
    def abrir_dialogue(pagamento: Pagamento):
        title_dialogue.value = f'Editar pagamento: {pagamento.conta_desc}'
        title_dialogue.data = pagamento
        drop_status_dialogue.value = pagamento.pago
        txt_valor_dialogue.value = f'{pagamento.valor:.2f}'.replace('.', ',')
        dialogue.open = True
        page.update()

    linha_selecao_data = ft.Column([
        ft.ResponsiveRow(
            [
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_BACK_ROUNDED),
                    on_click=voltar_data,
                    col={'xs': 3, 'md': 2, 'lg': 1},
                ),
                ft.Container(
                    content=txt_data_ano,
                    col={'xs': 3, 'md': 2, 'lg': 1},
                ),
                ft.Container(
                    content=txt_data_mes,
                    col={'xs': 3, 'md': 2, 'lg': 1},
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED),
                    on_click=avancar_data,
                    col={'xs': 3, 'md': 2, 'lg': 1},
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    ])

    carregar_data(int(txt_data_ano.value), int(txt_data_mes.value))
    bs_nova_conta = MyBsNovaConta(page, db, fatura.id, lambda: carregar_data(int(txt_data_ano.value), int(txt_data_mes.value))).bs
    page.overlay.append(dialogue)

    return ft.View(
        route='/contas',
        appbar=MyAppBar('ORCA - Orcamento Familiar', page),

        controls=[
            ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text('Minhas Contas', weight='bold', size=28),
                    ft.Divider(height=10, color='transparent'),
                    linha_selecao_data,
                    ft.Divider(height=15, color='transparent'),
                    ft.ResponsiveRow(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.ElevatedButton('Cadastrar Nova Conta', bgcolor=ft.Colors.BLUE_900, color='white', col={'xs': 10, 'md': 6}, on_click=lambda _: (setattr(bs_nova_conta, 'open', True), page.update()))
                        ]
                    ),
                    ft.Divider(height=80, thickness=1, color='grey'),
                    ft.Column(
                        controls=[
                            data_selecionada,
                            ft.Divider(height=20, color='transparent'),
                            ft.Container(
                                alignment=ft.alignment.center,
                                content=linha_exibicao_dados
                            )
                        ]
                    )
                ]),
            )
        ],

        scroll=ft.ScrollMode.AUTO
    )
