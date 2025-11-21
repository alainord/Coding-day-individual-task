import flet as ft
from smart_home import models


# ------------------------------
# Card para dispositivos ON/OFF
# ------------------------------
def _device_card(app, device: models.Device):
    # Colores por tipo de tarjeta
    bgcolor = (
        ft.Colors.YELLOW_100 if device.type == "switch" else ft.Colors.GREY_200
    )

    # Iconos compatibles con TODAS las versiones de Flet
    if device.type == "switch":
        icon_name = ft.Icons.LIGHT_MODE     # icono luz
    else:
        icon_name = ft.Icons.MEETING_ROOM   # icono puerta (seguro)

    icon = ft.Icon(icon_name, size=32, color=ft.Colors.BLUE_GREY_700)

    status_text = ft.Text(f"Status: {device.state}", size=14, color=ft.Colors.BLUE_GREY_700)

    # Acción principal según tipo de dispositivo
    if device.type == "switch":
        action_label = "Turn ON" if device.state == "OFF" else "Turn OFF"

        def on_click(e):
            new = "ON" if device.state == "OFF" else "OFF"
            models.set_device_state(device.id, new)
            app.show_overview()

    elif device.type == "lock":
        action_label = "Unlock" if device.state == "LOCKED" else "Lock"

        def on_click(e):
            new = "UNLOCKED" if device.state == "LOCKED" else "LOCKED"
            models.set_device_state(device.id, new)
            app.show_overview()
    else:
        action_label = None

    # Botones
    details_btn = ft.TextButton(
        "Details",
        on_click=lambda e: app.page.go(f"/device/{device.id}")
    )

    action_btn = ft.ElevatedButton(action_label, on_click=on_click)

    # TARJETA
    card = ft.Container(
        width=350,
        height=150,
        padding=15,
        bgcolor=bgcolor,
        border_radius=12,
        content=ft.Column(
            [
                ft.Row([icon, ft.Text(device.name, weight="bold", size=18)], spacing=10),
                status_text,
                ft.Row([details_btn, action_btn], alignment=ft.MainAxisAlignment.END)
            ],
            spacing=10
        )
    )

    return card


# ------------------------------
# Card para sliders (thermostat / fan)
# ------------------------------
def _slider_card(app, device: models.Device):

    # Colores pastel según tipo
    bgcolor = ft.Colors.PINK_50 if device.id == "thermostat" else ft.Colors.BLUE_100

    # Iconos compatibles
    if device.id == "thermostat":
        try:
            icon_name = ft.Icons.DEVICE_THERMOSTAT  # si existe
        except:
            icon_name = ft.Icons.AC_UNIT            # fallback seguro
    else:
        icon_name = ft.Icons.AUTORENEW  # No hay icono real de ventilador → este funciona bien

    icon = ft.Icon(icon_name, size=32, color=ft.Colors.BLUE_GREY_700)

    # Etiquetas
    label = ft.Text(
        f"Set point: {device.state} °C" if device.id == "thermostat" else f"Fan speed: {device.state}",
        size=14,
        color=ft.Colors.BLUE_GREY_700
    )

    # Slider
    slider = ft.Slider(
        min=0,
        max=30 if device.id == "thermostat" else 3,
        value=device.state,
        divisions=30 if device.id == "thermostat" else 3
    )

    def on_change(e):
        v = round(e.control.value, 1) if device.id == "thermostat" else int(e.control.value)
        models.set_device_value(device.id, v)
        app.show_overview()

    slider.on_change = on_change

    # TARJETA
    card = ft.Container(
        width=350,
        height=210,
        padding=15,
        bgcolor=bgcolor,
        border_radius=12,
        content=ft.Column([
            ft.Row([icon, ft.Text(device.name, weight="bold", size=18)], spacing=10),
            label,
            slider,
            ft.Row([
                ft.TextButton("Details", on_click=lambda e: app.page.go(f"/device/{device.id}"))
            ], alignment=ft.MainAxisAlignment.END)
        ], spacing=10)
    )

    return card


# ------------------------------
# VISTA PRINCIPAL (Overview)
# ------------------------------
def view(app):
    onoff_devices = [d for d in models.DEVICES.values() if d.type in ("switch", "lock")]
    slider_devices = [d for d in models.DEVICES.values() if d.type == "slider"]

    return ft.Column(
        [
            ft.Text("On/Off devices", size=22, weight="bold"),
            ft.Row(
                [_device_card(app, d) for d in onoff_devices],
                wrap=True,
                spacing=20,
                run_spacing=20
            ),

            ft.Divider(height=20),

            ft.Text("Slider controlled devices", size=22, weight="bold"),
            ft.Row(
                [_slider_card(app, d) for d in slider_devices],
                wrap=True,
                spacing=20,
                run_spacing=20
            ),
        ],
        scroll=ft.ScrollMode.AUTO
    )
