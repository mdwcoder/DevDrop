import flet as ft

class MessageItem(ft.Card):
    def __init__(self, page: ft.Page, plaintext: str):
        super().__init__()
        self.app_page = page
        self.plaintext = plaintext
        self.content_text = ft.Text("****", size=14, font_family="monospace")
        self.is_revealed = False

        self.reveal_btn = ft.IconButton(ft.Icons.VISIBILITY, on_click=self.toggle_reveal)
        self.copy_btn = ft.IconButton(ft.Icons.COPY, on_click=self.copy_content)
        
        self.content = ft.Container(
            padding=10,
            content=ft.Row([
                    self.content_text,
                    ft.Container(expand=True),
                    self.reveal_btn,
                    self.copy_btn
                ])
        )

    def toggle_reveal(self, e):
        self.is_revealed = not self.is_revealed
        self.content_text.value = self.plaintext if self.is_revealed else "****"
        self.reveal_btn.icon = ft.Icons.VISIBILITY_OFF if self.is_revealed else ft.Icons.VISIBILITY
        self.update()

    def copy_content(self, e):
        self.app_page.set_clipboard(self.plaintext)
        self.app_page.snack_bar = ft.SnackBar(ft.Text("Decrypted content copied!"))
        self.app_page.snack_bar.open = True
        self.app_page.update()


class ReceiveView(ft.Column):
    def __init__(self, page: ft.Page, session_controller):
        super().__init__(expand=True)
        self.app_page = page
        self.sc = session_controller
        self.input_text = ft.TextField(label="Paste Encrypted Message", multiline=True, min_lines=3, max_lines=5)
        self.messages_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        self.controls = [
            ft.Text("Receive Encrypted Message", weight="bold", size=20),
            self.input_text,
            ft.ElevatedButton("Decrypt", icon=ft.Icons.LOCK_OPEN, on_click=self.on_decrypt),
            ft.Divider(),
            ft.Text("Messages Inbox", weight="bold", size=18),
            self.messages_list
        ]

    def on_decrypt(self, e):
        val = self.input_text.value.strip()
        if not val:
            return
            
        try:
            msg_dict = self.sc.decrypt_message(val)
            payload = msg_dict.get("payload", "NO_PAYLOAD")
            
            # Add to list
            msg_item = MessageItem(self.app_page, payload)
            self.messages_list.controls.insert(0, msg_item)
            self.input_text.value = ""
            self.update()
            
            self.app_page.snack_bar = ft.SnackBar(ft.Text("Message decrypted successfully!"))
            self.app_page.snack_bar.open = True
            self.app_page.update()
        except Exception as ex:
            self.app_page.snack_bar = ft.SnackBar(ft.Text(f"Decryption failed: {ex}", color=ft.Colors.ERROR))
            self.app_page.snack_bar.open = True
            self.app_page.update()
