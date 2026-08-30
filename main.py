from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.uix.camera import Camera
from pyzbar import pyzbar
from PIL import Image
import io

KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)

    MDLabel:
        text: "Сканер Честного ЗНАКа"
        halign: "center"
        font_style: "H5"

    Camera:
        id: camera
        resolution: (640, 480)
        play: True

    MDFillRoundFlatButton:
        text: "Сканировать"
        pos_hint: {"center_x": 0.5}
        on_release: app.scan_code()

    MDTextField:
        id: code_input
        hint_text: "Код (можно вставить)"
        mode: "rectangle"
        multiline: True
        size_hint_y: None
        height: dp(60)

    MDFillRoundFlatButton:
        text: "Сгенерировать код"
        pos_hint: {"center_x": 0.5}
        on_release: app.generate_code()
'''

class CZScannerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def scan_code(self):
        camera = self.root.ids.camera
        texture = camera.texture
        if not texture:
            self.show_dialog("❌ Камера не доступна")
            return

        buf = texture.pixels
        width, height = texture.size
        pil_image = Image.frombytes(mode='RGBA', size=(width, height), data=buf)
        pil_image = pil_image.convert('L')

        decoded = pyzbar.decode(pil_image)
        if decoded:
            data = decoded[0].data.decode('utf-8')
            escaped_data = repr(data).strip("'")
            self.root.ids.code_input.text = escaped_data
            self.show_dialog(f"✅ Найден код:\n{escaped_data}")
        else:
            self.show_dialog("❌ Код не распознан")

    def generate_code(self):
        import qrcode
        import os
        from kivy.utils import platform
        raw_text = self.root.ids.code_input.text
        try:
            code_data = raw_text.encode('utf-8').decode('unicode_escape')
        except:
            self.show_dialog("❌ Ошибка в формате кода")
            return

        try:
            qr = qrcode.QRCode(border=0)
            qr.add_data(code_data, optimize=0)
            matrix = qr.get_matrix()

            size = 300
            img = Image.new('1', (size, size), 1)
            pixel_size = size // len(matrix)
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if cell:
                        for dy in range(pixel_size):
                            for dx in range(pixel_size):
                                img.putpixel((x * pixel_size + dx, y * pixel_size + dy), 0)

            # Сохраняем в папку загрузок
            if platform == 'android':
                from android.storage import primary_external_storage_path
                dir_path = primary_external_storage_path()
            else:
                dir_path = os.path.expanduser("~")

            file_path = os.path.join(dir_path, "cz_datamatrix.png")
            img.save(file_path)
            self.show_dialog(f"✅ Код сохранён:\n{file_path}")
        except Exception as e:
            self.show_dialog(f"❌ Ошибка: {str(e)}")

    def show_dialog(self, text):
        self.dialog = MDDialog(
            text=text,
            buttons=[
                MDFlatButton(text="OK", on_release=lambda x: self.dialog.dismiss())
            ],
        )
        self.dialog.open()

CZScannerApp().run()
