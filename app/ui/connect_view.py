import flet as ft
from core.session import SessionState

class ConnectView(ft.Column):
    def __init__(self, page: ft.Page, session_controller, on_status_change):
        super().__init__(scroll=ft.ScrollMode.AUTO)
        self.app_page = page
        self.sc = session_controller
        self.on_status_change = on_status_change
        
        self.offer_text = ft.TextField(label="Generated Offer", multiline=True, read_only=True, min_lines=3, max_lines=5)
        self.answer_input = ft.TextField(label="Paste Answer/Offer Here", multiline=True, min_lines=3, max_lines=5)
        self.fingerprint_text = ft.Text("No Fingerprint", size=16, weight="bold", color=ft.Colors.GREEN, visible=False)

        self.controls = [
            ft.Text("A) Create Session", weight="bold", size=18),
            ft.ElevatedButton("Create Session", on_click=self.on_create_session),
            ft.Divider(),
            
            ft.Text("B) Offer", weight="bold", size=18),
            self.offer_text,
            ft.ElevatedButton("Copy Offer", icon=ft.Icons.COPY, on_click=self.copy_offer),
            ft.Divider(),

            ft.Text("C) Paste Answer / Peer Offer", weight="bold", size=18),
            self.answer_input,
            ft.ElevatedButton("Process / Connect", on_click=self.on_process),
            ft.Divider(),

            ft.Text("D) Fingerprint", weight="bold", size=18),
            self.fingerprint_text
        ]

    def on_create_session(self, e):
        try:
            offer_str = self.sc.generate_offer()
            self.offer_text.value = offer_str
            self.on_status_change("OFFER CREATED", ft.Colors.BLUE)
            self.update()
        except Exception as ex:
            self._show_error(str(ex))

    def copy_offer(self, e):
        if self.offer_text.value:
            self.app_page.set_clipboard(self.offer_text.value)
            self._show_snack("Offer copied to clipboard!")

    def on_process(self, e):
        val = self.answer_input.value.strip()
        if not val:
            return
        
        try:
            if self.sc.session.state == SessionState.OFFER_CREATED:
                self.sc.process_answer(val)
                self.on_status_change("CONNECTED", ft.Colors.GREEN)
                self._show_fingerprint()
            else:
                answer_str = self.sc.process_offer_generate_answer(val)
                self.offer_text.value = answer_str
                self.on_status_change("CONNECTED (Generated Answer)", ft.Colors.GREEN)
                self._show_snack("Answer generated! Copy and return it to peer.")
                self._show_fingerprint()
            self.update()
        except Exception as ex:
            self._show_error(f"Error processing: {ex}")

    def reset(self):
        self.offer_text.value = ""
        self.answer_input.value = ""
        self.fingerprint_text.visible = False
        self.update()

    def _show_fingerprint(self):
        if self.sc.session.fingerprint:
            self.fingerprint_text.value = self.sc.session.fingerprint
            self.fingerprint_text.visible = True

    def _show_snack(self, msg):
        self.app_page.snack_bar = ft.SnackBar(ft.Text(msg))
        self.app_page.snack_bar.open = True
        self.app_page.update()

    def _show_error(self, msg):
        self.app_page.snack_bar = ft.SnackBar(ft.Text(msg, color=ft.Colors.ERROR))
        self.app_page.snack_bar.open = True
        self.app_page.update()
