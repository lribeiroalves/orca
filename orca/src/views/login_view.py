import flet as ft
from database import Database
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from typing import Callable
import os

def login_view(page: ft.Page, db: Database, ao_confirmar: Callable=lambda: print('OK'), block: bool=True):
    unlock_pass = db.get_block_pass() # Se falso, a senha esta bloqueada
    if not block:
        ao_confirmar()
    load_dotenv()
    PIN_DIGIT = int(os.getenv('PIN_DIGIT'))
    pin_atual = ""
    counter_errors = 0 # contagem de senhas erradas
    icone_cadeado = ft.Icon(ft.Icons.LOCK_PERSON, size=80, color=ft.Colors.BLUE_900 if unlock_pass else ft.Colors.RED_900)

    # Espaços visuais (bolinhas) para o PIN
    indicadores = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[ft.Icon(ft.Icons.CIRCLE, size=20, color="grey") for _ in range(PIN_DIGIT)]
    )

    def atualizar_indicadores():
        for i, icon in enumerate(indicadores.controls):
            if i < len(pin_atual):
                icon.name = ft.Icons.CIRCLE
                icon.color = ft.Colors.BLUE_900
            else:
                icon.name = ft.Icons.CIRCLE
                icon.color = "grey"
        page.update()

    def digitar_numero(e):
        nonlocal unlock_pass
        if unlock_pass:
            nonlocal pin_atual
            if len(pin_atual) < PIN_DIGIT:
                pin_atual += e.control.text
                atualizar_indicadores()
                
                if len(pin_atual) == PIN_DIGIT:
                    validar_pin()

    def limpar_pin(e):
        nonlocal pin_atual
        if pin_atual == "":
            page.on_view_pop(None)
        pin_atual = ""
        atualizar_indicadores()

    def validar_pin():
        nonlocal counter_errors
        nonlocal unlock_pass
        if unlock_pass:
            if check_password_hash(db.get_password(), pin_atual):
                limpar_pin(None)
                ao_confirmar() # Função que libera o acesso
            else:
                page.open(ft.SnackBar(ft.Text("PIN Incorreto!", color="white"), bgcolor="red"))
                limpar_pin(None)
                counter_errors += 1
                if counter_errors >= 10:
                    db.block_pass()
                    unlock_pass = False
                    icone_cadeado.color = ft.Colors.RED_900
                    page.update()

    # Função para criar os botões do teclado de forma padronizada
    def btn_num(num):
        return ft.ElevatedButton(
            text=str(num),
            on_click=digitar_numero,
            style=ft.ButtonStyle(
                shape=ft.CircleBorder(),
                padding=25,
                text_style=ft.TextStyle(size=25, weight="bold"),
            ),
            disabled=True if not unlock_pass else False
        )

    return ft.View(
        "/login",
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            icone_cadeado,
            ft.Text("Controle de Acesso", size=28, weight="bold"),
            ft.Text("Digite seu PIN de acesso", color="grey"),
            ft.Container(height=20),
            indicadores,
            ft.Container(height=20),
            # Layout do Teclado
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[btn_num(1), btn_num(2), btn_num(3)]),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[btn_num(4), btn_num(5), btn_num(6)]),
                    ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[btn_num(7), btn_num(8), btn_num(9)]),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER, 
                        controls=[
                            ft.IconButton(ft.Icons.BACKSPACE, on_click=limpar_pin, icon_size=30, disabled=True if not unlock_pass else False),
                            btn_num(0),
                            ft.IconButton(ft.Icons.CHECK_CIRCLE, icon_color="green", icon_size=40, on_click=lambda _: validar_pin(), disabled=True if not unlock_pass else False)
                        ]
                    ),
                ]
            )
        ]
    )
