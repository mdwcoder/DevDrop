import flet as ft
from core.session import SessionState

class SendView(ft.Column):
    def __init__(self, page: ft.Page, session_controller):
        super().__init__(scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        self.sc = session_controller
        self.input_text = ft.TextField(label="Message Payload", multiline=True, min_lines=4, max_lines=10)
        self.one_time_check = ft.Checkbox(label="One-Time View (UI V1)", value=True)
        self.output_text = ft.TextField(label="Encrypted Output", multiline=True, read_only=True, min_lines=3, max_lines=5)

        self.controls = [
            ft.Text("Send Encrypted Message", weight="bold", size=20),
            self.input_text,
            self.one_time_check,
            ft.ElevatedButton("Encrypt & Send", icon=ft.Icons.LOCK, on_click=self.on_send),
            ft.Divider(),
            self.output_text,
            ft.ElevatedButton("Copy Output", icon=ft.Icons.COPY, on_click=self.copy_output)
        ]

    def on_send(self, e):
        if self.sc.session.state != SessionState.CONNECTED:
            self.app_page.snack_bar = ft.SnackBar(ft.Text("Cannot send: Session is not CONNECTED", color=ft.Colors.ERROR))
            self.app_page.snack_bar.open = True
            self.app_page.update()
            return

        payload = self.input_text.value
        if not payload:
            return

        try:
            encrypted_str = self.sc.encrypt_message(payload)
            self.output_text.value = encrypted_str
            self.input_text.value = ""
            self.update()
        except Exception as ex:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Encryption failed: {ex}", color=ft.Colors.ERROR))
            self.app_page.snack_bar.open = True
            self.app_page.update()

    def copy_output(self, e):
        if self.output_text.value:
            self.app_page.set_clipboard(self.output_text.value)
            self.app_page.snack_bar = ft.SnackBar(ft.Text("Encrypted message copied!"))
            self.app_page.snack_bar.open = True
            self.app_page.update()
