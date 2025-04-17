from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.window import Window
import os
import cv2
from pyzbar.pyzbar import decode
from kivy.graphics.texture import Texture

SIGNS_DIR = os.path.join(os.getcwd(), 'traffic_signs')

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.img_widget = KivyImage(size_hint=(1, 0.7))
        self.add_widget(self.img_widget)
        self.label = Label(text='وجّه رمز QR نحو الكاميرا', size_hint=(1, 0.1))
        self.add_widget(self.label)
        self.btn = Button(text='تشغيل الكاميرا لمسح QR', size_hint=(1, 0.2))
        self.btn.bind(on_press=self.start_camera)
        self.add_widget(self.btn)
        self.capture = None
        self.scanning = False

    def start_camera(self, instance):
        if not self.scanning:
            self.capture = cv2.VideoCapture(0)
            self.scanning = True
            self.label.text = 'جاري المسح...'
            Clock.schedule_interval(self.update, 1.0/30.0)

    def update(self, dt):
        if self.capture is not None and self.scanning:
            ret, frame = self.capture.read()
            if ret:
                # عرض الكاميرا
                buf = cv2.flip(frame, 0).tobytes()
                img_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
                img_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                self.img_widget.texture = img_texture
                # محاولة قراءة QR
                decoded_objs = decode(frame)
                if decoded_objs:
                    qr_data = decoded_objs[0].data.decode('utf-8')
                    img_path = os.path.join(SIGNS_DIR, qr_data)
                    if os.path.exists(img_path):
                        self.img_widget.source = img_path
                        self.label.text = f'تم عرض الصورة: {qr_data}'
                    else:
                        self.label.text = 'لم يتم العثور على صورة اللوحة!'
                    self.stop_camera()

    def stop_camera(self):
        if self.capture:
            self.capture.release()
            self.capture = None
        self.scanning = False
        Clock.unschedule(self.update)

class TrafficSignApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainLayout()

if __name__ == '__main__':
    TrafficSignApp().run()
