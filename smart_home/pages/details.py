import flet as ft
from smart_home import models


def view(app, device_id: str):
    d = models.DEVICES.get(device_id)
    if not d:
        return ft.Column([ft.Text("Device not found"), ft.ElevatedButton("Back to overview", on_click=lambda e: app.page.go("/"))])

    actions = models.get_recent_actions(device_id=device_id, limit=10)
    action_texts = [ft.Text(f"{a['time']} - {a['action']} ({a['user']})") for a in actions]

    return ft.Column([
        ft.Text(f"{d.name} details", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text(f"ID: {d.id}"),
        ft.Text(f"Type: {d.type}"),
        ft.Text(f"State: {d.state}"),
        ft.Divider(),
        ft.Text("Recent actions", weight=ft.FontWeight.BOLD),
        ft.Column(action_texts),
        ft.ElevatedButton("Back to overview", on_click=lambda e: app.page.go("/")),
    ], scroll=ft.ScrollMode.AUTO)
