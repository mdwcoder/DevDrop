import flet as ft

def create_header(page: ft.Page, on_new_session, on_toggle_pin):
    status_text = ft.Text("INIT", weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE)

    def on_pin_click(e):
        page.window.always_on_top = not page.window.always_on_top
        page.update()
        on_toggle_pin(page.window.always_on_top)

    def update_status(new_status: str, color: str):
        status_text.value = new_status
        status_text.color = color
        status_text.update()

    app_bar = ft.AppBar(
        leading=ft.Icon(ft.Icons.SHIELD),
        leading_width=40,
        title=ft.Row([
            ft.Text("DevDrop"),
            ft.Text(" | Status: "),
            status_text
        ]),
        center_title=False,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        actions=[
            ft.IconButton(ft.Icons.ADD, tooltip="New Session", on_click=lambda e: on_new_session()),
            ft.IconButton(ft.Icons.PUSH_PIN, tooltip="Toggle Pin (Always on top)", on_click=on_pin_click),
            ft.IconButton(ft.Icons.MINIMIZE, tooltip="Minimize", on_click=lambda e: setattr(page.window, 'minimized', True) or page.update()),
        ]
    )
    return app_bar, update_status
