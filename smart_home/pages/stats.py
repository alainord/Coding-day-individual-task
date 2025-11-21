import flet as ft
from smart_home import models
import threading
import time

# Historial de consumos (vacío al inicio)
history = []
background_thread_started = False


def view(app):

    page = app.page

    # ----------------------------------------------------
    # FUNCIÓN: Calcular consumo actual real
    # ----------------------------------------------------
    def calculate_power_usage():
        total = 0
        for dev in models.DEVICES.values():

            if dev.type == "switch" and dev.state == "ON":
                total += 10

            elif dev.type == "lock" and dev.state == "UNLOCKED":
                total += 2

            elif dev.type == "slider":
                if dev.id == "thermostat":
                    total += dev.state * 5
                elif dev.id == "ceiling_fan":
                    total += dev.state * 20

        return total

    # ----------------------------------------------------
    # FUNCIÓN: Construir gráfico
    # ----------------------------------------------------
    def build_graph():
        if not history:
            return ft.Text("Waiting for first datapoint… (10s)", italic=True)

        max_value = max(history) if history else 1

        bars = []
        for val in history:
            pct = val / max_value if max_value else 0
            bars.append(
                ft.Container(
                    height=100 * pct + 5,
                    width=10,
                    bgcolor=ft.Colors.BLUE_300,
                    border_radius=6,
                )
            )

        return ft.Row(bars, spacing=4, vertical_alignment="end")

    # Contenedor del gráfico
    graph_container = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_400),
        padding=10,
        height=200,
        expand=True,
        content=build_graph(),
    )

    # ----------------------------------------------------
    # THREADING: Ejecutar cada 10 segundos
    # ----------------------------------------------------
    def background_worker():
        while True:
            time.sleep(10)
            new_val = calculate_power_usage()
            history.append(new_val)

            # Limitar historial
            if len(history) > 100:
                history.pop(0)

            graph_container.content = build_graph()
            page.update()

    global background_thread_started
    if not background_thread_started:
        t = threading.Thread(target=background_worker, daemon=True)
        t.start()
        background_thread_started = True

    # ----------------------------------------------------
    # TABLA DE LOGS
    # ----------------------------------------------------
    rows = []
    for a in models.get_recent_actions(limit=20):
        rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(a["time"])),
                    ft.DataCell(ft.Text(a["device"])),
                    ft.DataCell(ft.Text(a["action"])),
                    ft.DataCell(ft.Text(a["user"])),
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Time")),
            ft.DataColumn(ft.Text("Device")),
            ft.DataColumn(ft.Text("Action")),
            ft.DataColumn(ft.Text("User")),
        ],
        rows=rows,
    )

    # ----------------------------------------------------
    # LAYOUT FINAL
    # ----------------------------------------------------
    return ft.Column(
        [
            ft.Text("Power consumption history", size=20, weight="bold"),
            graph_container,
            ft.Divider(),
            ft.Text("Action log", size=20, weight="bold"),
            ft.Container(content=table, padding=10, bgcolor=ft.Colors.WHITE, border_radius=6),
        ],
        scroll=ft.ScrollMode.AUTO,
    )
