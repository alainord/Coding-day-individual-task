import flet as ft
from smart_home import models
from smart_home.pages import overview, stats, details


class SmartHomeApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = ft.Container()

    def build(self):
        self.page.on_route_change = self.on_route_change
        self.page.go("/")
        self.page.appbar = ft.AppBar(
            title=ft.Text("Smart Home Controller"),
            actions=[
                ft.TextButton("Overview", on_click=lambda e: self.page.go("/")),
                ft.TextButton("Statistics", on_click=lambda e: self.page.go("/stats")),
                ft.TextButton("Rooms", on_click=lambda e: self.page.go("/rooms")), 
            ],
        )

        self.page.add(self.content)
        # go to initial
        if not self.page.route:
            self.page.go("/")

    def on_route_change(self, route):
        r = self.page.route
        # simple routing
        if r == "/" or r == "":
            self.show_overview()
        elif r == "/stats":
            self.show_stats()
        elif r == "/rooms":
            self.show_rooms()

        elif r.startswith("/device/"):
            did = r.split("/device/", 1)[1]
            self.show_device_details(did)

    def show_overview(self):
        self.content.content = overview.view(self)
        self.page.update()

    def show_stats(self):
        self.content.content = stats.view(self)
        self.page.update()

    def show_device_details(self, device_id: str):
        self.content.content = details.view(self, device_id)
        self.page.update()
        
    def show_rooms(self):
        import smart_home.pages.rooms as rooms
        self.content.content = rooms.view(self)
        self.page.update()