import flet as ft
from smart_home import models


def view(app):

    page = app.page

    # ===========================================
    # DIALOG: ADD ROOM
    # ===========================================

    name_field = ft.TextField(label="Room name", autofocus=True)

    def close_add_room(e=None):
        add_room_dialog.open = False
        page.update()

    def add_room(e=None):
        name = name_field.value.strip()
        if name:
            models.add_room(name)
        close_add_room()
        refresh()

    add_room_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add new room"),
        content=name_field,
        actions=[
            ft.TextButton("Cancel", on_click=close_add_room),
            ft.FilledButton("Add", on_click=add_room),
        ],
    )
    page.overlay.append(add_room_dialog)

    def open_add_room(e):
        name_field.value = ""
        add_room_dialog.open = True
        page.update()

    # ===========================================
    # DIALOG: ADD DEVICE
    # ===========================================

    device_name = ft.TextField(label="Device name")
    device_type = ft.Dropdown(
        label="Device type",
        options=[
            ft.dropdown.Option("switch"),
            ft.dropdown.Option("slider"),
            ft.dropdown.Option("lock"),
        ],
    )

    def close_add_device(e=None):
        add_device_dialog.open = False
        page.update()

    def confirm_add_device(e=None):
        if device_name.value and device_type.value:
            models.create_device(device_name.value, device_type.value)
        close_add_device()
        refresh()

    add_device_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Add new device"),
        content=ft.Column([device_name, device_type]),
        actions=[
            ft.TextButton("Cancel", on_click=close_add_device),
            ft.FilledButton("Create", on_click=confirm_add_device),
        ],
    )
    page.overlay.append(add_device_dialog)

    def open_add_device(e):
        device_name.value = ""
        device_type.value = None
        add_device_dialog.open = True
        page.update()

    # ===========================================
    # DIALOG: ASSIGN DEVICE
    # ===========================================

    def open_assign_dialog(room_name: str):
        room = models._find_room(room_name)
        assigned = set(room["device_ids"])
        available = [d for d in models.DEVICES.values() if d.id not in assigned]

        device_dd = ft.Dropdown(
            label="Select device",
            options=[ft.dropdown.Option(d.id) for d in available],
        )

        def cancel(e=None):
            assign_dialog.open = False
            page.update()

        def confirm(e=None):
            if device_dd.value:
                models.assign_device_to_room(room_name, device_dd.value)
            assign_dialog.open = False
            page.update()
            refresh()

        assign_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Assign device to {room_name}"),
            content=device_dd,
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.FilledButton("Assign", on_click=confirm),
            ],
        )

        page.overlay.append(assign_dialog)
        assign_dialog.open = True
        page.update()

    # ===========================================
    # REMOVE DEVICE FROM ROOM
    # ===========================================

    def remove_device(room_name: str, device_id: str):
        models.remove_device_from_room(room_name, device_id)
        refresh()

    # ===========================================
    # OVERVIEW FILTER
    # ===========================================

    filter_dd = ft.Dropdown(
        label="Filter by room",
        options=[ft.dropdown.Option("All")] +
                [ft.dropdown.Option(r["name"]) for r in models.get_rooms()],
        value="All",
        on_change=lambda e: refresh(),
    )

    rooms_list = ft.Column()

    # ===========================================
    # REFRESH UI
    # ===========================================

    def refresh():
        rooms_list.controls = []
        rooms = models.get_rooms()
        selected = filter_dd.value

        for r in rooms:
            room_name = r["name"]

            if selected != "All" and selected != room_name:
                continue

            devices = models.get_devices_in_room(room_name)

            device_widgets = []
            for d in devices:
                device_widgets.append(
                    ft.Row(
                        [
                            ft.Text(f"{d.name} ({d.type})"),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                tooltip="Remove device",
                                on_click=lambda e, rn=room_name, did=d.id: remove_device(rn, did),
                                icon_color=ft.Colors.RED,
                            )
                        ],
                        alignment="spaceBetween",
                    )
                )

            room_card = ft.Container(
                content=ft.Column([
                    ft.Row(
                        [
                            ft.Text(room_name, size=20, weight="bold"),
                            ft.FilledButton(
                                "Assign device",
                                icon=ft.Icons.DEVICE_HUB,
                                on_click=lambda e, rn=room_name: open_assign_dialog(rn),
                            )
                        ], alignment="spaceBetween",
                    ),
                    ft.Divider(),
                    ft.Column(device_widgets) if device_widgets
                    else ft.Text("No devices assigned", italic=True),
                ]),
                padding=15,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                border=ft.border.all(1, ft.Colors.GREY_300),
                margin=ft.margin.only(bottom=15)
            )

            rooms_list.controls.append(room_card)

        # update filter options dynamically
        filter_dd.options = [ft.dropdown.Option("All")] + \
                             [ft.dropdown.Option(r["name"]) for r in models.get_rooms()]

        page.update()

    refresh()

    # ===========================================
    # MAIN LAYOUT
    # ===========================================

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Text("Rooms overview", size=26, weight="bold"),
                    ft.FilledButton("Add Room", icon=ft.Icons.ADD, on_click=open_add_room),
                    ft.FilledButton("Add Device", icon=ft.Icons.ADD_BOX, on_click=open_add_device),
                ],
                alignment="spaceBetween",
            ),
            filter_dd,
            ft.Divider(),
            rooms_list
        ],
        scroll=ft.ScrollMode.AUTO
    )
