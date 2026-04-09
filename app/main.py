"""
Interfaz principal de la aplicación Flet para billetera digital.
Diseño mobile-first con navegación por pestañas.
"""
import flet as ft
from app.models import init_db
from app.services import CuentaService, MovimientoService


def main(page: ft.Page):
    # Configuración de la página para móvil
    page.title = "Mi Billetera"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    # Inicializar base de datos
    init_db()

    # Estado de la aplicación
    selected_cuenta_id = None

    # === VISTA DE INICIO ===
    def crear_vista_inicio():
        """Crea la vista principal con resumen de cuentas"""
        
        def actualizar_resumen():
            """Actualiza el resumen de cuentas"""
            cuentas = CuentaService.obtener_todas_las_cuentas()
            total_saldo = sum(c.saldo_actual for c in cuentas)
            
            # Tarjeta de saldo total
            tarjeta_total = ft.Container(
                content=ft.Column([
                    ft.Text("Saldo Total", size=14, color=ft.colors.WHITE70),
                    ft.Text(f"${total_saldo:,.2f}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(f"{len(cuentas)} cuentas", size=12, color=ft.colors.WHITE54),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.START),
                gradient=ft.LinearGradient(
                    colors=[ft.colors.BLUE_700, ft.colors.PURPLE_600],
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                ),
                padding=20,
                border_radius=16,
                margin=ft.margin.only(left=16, right=16, top=16, bottom=8),
            )

            # Lista de cuentas
            lista_cuentas = []
            for cuenta in cuentas:
                item = ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Icon(
                            ft.icons.ACCOUNT_BALANCE_WALLET if cuenta.tipo == "general" 
                            else ft.icons.SAVINGS,
                            color=ft.colors.WHITE
                        ),
                        bgcolor=ft.colors.BLUE if cuenta.tipo == "general" else ft.colors.GREEN,
                    ),
                    title=ft.Text(cuenta.nombre, weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(f"{cuenta.tipo.capitalize()}", size=12),
                    trailing=ft.Text(
                        f"${cuenta.saldo_actual:,.2f}",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.colors.GREEN if cuenta.saldo_actual >= 0 else ft.colors.RED,
                    ),
                    on_click=lambda e, cid=cuenta.id: navegar_a_movimientos(cid),
                )
                lista_cuentas.append(item)

            return ft.Column([
                tarjeta_total,
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Mis Cuentas", size=18, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                icon_size=24,
                                on_click=lambda e: mostrar_dialogo_nueva_cuenta()
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ] + lista_cuentas if lista_cuentas else [
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET_OUTLINED, size=48, color=ft.colors.GREY_400),
                                ft.Text("No hay cuentas", color=ft.colors.GREY_600),
                                ft.Text("Toca + para agregar tu primera cuenta", size=12, color=ft.colors.GREY_500),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=40,
                        )
                    ]),
                    padding=16,
                ),
            ], scroll=ft.ScrollMode.AUTO, expand=True)

        vista = actualizar_resumen()
        return vista

    # === VISTA DE MOVIMIENTOS ===
    def crear_vista_movimientos():
        """Crea la vista de movimientos de una cuenta específica"""
        
        def cargar_movimientos():
            """Carga los movimientos de la cuenta seleccionada"""
            if not selected_cuenta_id:
                return ft.Container()
            
            cuenta = CuentaService.obtener_cuenta_por_id(selected_cuenta_id)
            if not cuenta:
                return ft.Container()
            
            movimientos = MovimientoService.obtener_movimientos_por_cuenta(selected_cuenta_id)
            
            lista_movimientos = []
            for mov in movimientos:
                es_ingreso = mov.tipo == "ingreso"
                item = ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Icon(
                            ft.icons.ARROW_DOWNWARD if es_ingreso else ft.icons.ARROW_UPWARD,
                            color=ft.colors.WHITE,
                            size=20
                        ),
                        bgcolor=ft.colors.GREEN if es_ingreso else ft.colors.RED,
                    ),
                    title=ft.Text(mov.descripcion or "Sin descripción", weight=ft.FontWeight.W_500),
                    subtitle=ft.Text(
                        f"{mov.categoria or 'General'} • {mov.fecha.strftime('%d/%m/%Y %H:%M')}",
                        size=12
                    ),
                    trailing=ft.Text(
                        f"+${mov.monto:,.2f}" if es_ingreso else f"-${mov.monto:,.2f}",
                        weight=ft.FontWeight.BOLD,
                        size=16,
                        color=ft.colors.GREEN if es_ingreso else ft.colors.RED,
                    ),
                )
                lista_movimientos.append(item)

            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda e: volver_al_inicio()
                            ),
                            ft.Text(cuenta.nombre, size=20, weight=ft.FontWeight.BOLD),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(),
                        ft.Row([
                            ft.Text("Saldo Actual", size=14),
                            ft.Text(
                                f"${cuenta.saldo_actual:,.2f}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.GREEN if cuenta.saldo_actual >= 0 else ft.colors.RED,
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ]),
                    padding=16,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Movimientos Recientes", size=16, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD_CIRCLE,
                                icon_color=ft.colors.BLUE,
                                on_click=lambda e: mostrar_dialogo_nuevo_movimiento()
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ] + lista_movimientos if lista_movimientos else [
                        ft.Container(
                            content=ft.Column([
                                ft.Icon(ft.icons.RECEIPT_LONG_OUTLINED, size=48, color=ft.colors.GREY_400),
                                ft.Text("Sin movimientos", color=ft.colors.GREY_600),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            padding=40,
                        )
                    ]),
                    padding=16,
                ),
            ], scroll=ft.ScrollMode.AUTO, expand=True)

        vista = cargar_movimientos()
        return vista

    # === NAVEGACIÓN ===
    def navegar_a_movimientos(cuenta_id):
        """Navega a la vista de movimientos de una cuenta"""
        nonlocal selected_cuenta_id
        selected_cuenta_id = cuenta_id
        page.views.clear()
        page.views.append(crear_vista_movimientos())
        page.update()

    def volver_al_inicio():
        """Vuelve a la vista de inicio"""
        nonlocal selected_cuenta_id
        selected_cuenta_id = None
        page.views.clear()
        page.views.append(crear_vista_inicio())
        page.update()

    # === DIÁLOGOS ===
    def mostrar_dialogo_nueva_cuenta():
        """Muestra diálogo para crear nueva cuenta"""
        nombre_field = ft.TextField(label="Nombre de la cuenta", hint_text="Ej: Efectivo, Banco X")
        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("general", "General"),
                ft.dropdown.Option("ahorro", "Ahorro"),
                ft.dropdown.Option("credito", "Crédito"),
            ],
            value="general"
        )
        saldo_field = ft.TextField(label="Saldo inicial", hint_text="0", keyboard_type=ft.KeyboardType.NUMBER)

        def guardar_cuenta(e):
            if not nombre_field.value:
                nombre_field.error_text = "El nombre es requerido"
                nombre_field.update()
                return
            
            try:
                saldo = float(saldo_field.value or 0)
            except ValueError:
                saldo_field.error_text = "Ingrese un número válido"
                saldo_field.update()
                return

            CuentaService.crear_cuenta(
                nombre=nombre_field.value,
                tipo=tipo_dropdown.value,
                saldo_inicial=saldo
            )
            
            dlg.open = False
            volver_al_inicio()

        dlg = ft.AlertDialog(
            title=ft.Text("Nueva Cuenta"),
            content=ft.Column([nombre_field, tipo_dropdown, saldo_field], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dlg()),
                ft.FilledButton("Guardar", on_click=guardar_cuenta),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def close_dlg():
            dlg.open = False
            page.update()

        page.dialog = dlg
        dlg.open = True
        page.update()

    def mostrar_dialogo_nuevo_movimiento():
        """Muestra diálogo para registrar nuevo movimiento"""
        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("ingreso", "Ingreso"),
                ft.dropdown.Option("gasto", "Gasto"),
            ],
            value="gasto"
        )
        monto_field = ft.TextField(label="Monto", hint_text="0", keyboard_type=ft.KeyboardType.NUMBER)
        descripcion_field = ft.TextField(label="Descripción", hint_text="Ej: Compras supermercado")
        categoria_field = ft.TextField(label="Categoría", hint_text="Ej: Alimentos, Transporte")

        def guardar_movimiento(e):
            try:
                monto = float(monto_field.value)
            except (ValueError, TypeError):
                monto_field.error_text = "Ingrese un monto válido"
                monto_field.update()
                return

            if not selected_cuenta_id:
                return

            MovimientoService.registrar_movimiento(
                cuenta_id=selected_cuenta_id,
                tipo=tipo_dropdown.value,
                monto=monto,
                descripcion=descripcion_field.value,
                categoria=categoria_field.value
            )

            dlg.open = False
            page.views.clear()
            page.views.append(crear_vista_movimientos())
            page.update()

        dlg = ft.AlertDialog(
            title=ft.Text("Nuevo Movimiento"),
            content=ft.Column([tipo_dropdown, monto_field, descripcion_field, categoria_field], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: close_dlg()),
                ft.FilledButton("Guardar", on_click=guardar_movimiento),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def close_dlg():
            dlg.open = False
            page.update()

        page.dialog = dlg
        dlg.open = True
        page.update()

    # Inicializar vista
    page.views.append(crear_vista_inicio())
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
