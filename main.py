import flet as ft
from app.ui.main_window import main_window

def main(page: ft.Page):
    main_window(page)

if __name__ == "__main__":
    ft.app(target=main)
