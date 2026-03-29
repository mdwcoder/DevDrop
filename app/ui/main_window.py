import flet as ft
from app.controllers.session_controller import SessionController
from app.ui.header import create_header
from app.ui.connect_view import ConnectView
from app.ui.send_view import SendView
from app.ui.receive_view import ReceiveView
from storage.settings_store import SettingsStore

def main_window(page: ft.Page):
    page.title = "DevDrop"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 600
    page.window.height = 750
    page.window.min_width = 400
    page.window.min_height = 500
    
    # Load settings
    settings = SettingsStore.load()
    if "window_width" in settings:
        page.window.width = settings["window_width"]
    if "window_height" in settings:
        page.window.height = settings["window_height"]
    if "window_top" in settings:
        page.window.top = settings["window_top"]
    if "window_left" in settings:
        page.window.left = settings["window_left"]
    if "always_on_top" in settings:
        page.window.always_on_top = settings["always_on_top"]

    # Controller
    sc = SessionController()

    app_bar = None
    update_status = None

    # Callbacks
    def on_new_session():
        sc.reset_session()
        connect_view.reset()
        update_status("INIT", ft.Colors.ORANGE)

    def on_toggle_pin(is_pinned: bool):
        settings["always_on_top"] = is_pinned
        SettingsStore.save(settings)

    def on_window_event(e):
        if e.data == "close":
            try:
                settings["window_width"] = page.window.width
                settings["window_height"] = page.window.height
                settings["window_top"] = page.window.top
                settings["window_left"] = page.window.left
                SettingsStore.save(settings)
            except Exception as ex:
                print(f"Error saving settings: {ex}")
            finally:
                page.window.destroy()

    page.window.prevent_close = False
    page.window.on_event = on_window_event

    # Header
    app_bar, update_status = create_header(page, on_new_session, on_toggle_pin)
    page.appbar = app_bar

    # Views
    connect_view = ConnectView(page, sc, update_status)
    send_view = SendView(page, sc)
    receive_view = ReceiveView(page, sc)

    # Navigation Layout
    main_content = ft.Container(content=connect_view, padding=20, expand=True)

    def on_nav_change(e):
        idx = e.control.selected_index
        if idx == 0:
            main_content.content = connect_view
        elif idx == 1:
            main_content.content = send_view
        else:
            main_content.content = receive_view
        main_content.update()

    nav_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.CABLE, label="Connect"),
            ft.NavigationBarDestination(icon=ft.Icons.SEND, label="Send"),
            ft.NavigationBarDestination(icon=ft.Icons.INBOX, label="Receive")
        ],
        on_change=on_nav_change,
        selected_index=0
    )
    
    page.add(ft.Column([nav_bar, main_content], expand=True))
