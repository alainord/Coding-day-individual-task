import flet as ft
from smart_home.app import SmartHomeApp


def main(page: ft.Page):
    page.title = "Smart Home Controller"
    page.window_width = 1000
    page.window_height = 700
    app = SmartHomeApp(page)
    app.build()


if __name__ == "__main__":
    ft.app(target=main)
