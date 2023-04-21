from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.texture import Texture
from PIL import Image as img
from PIL import ImageFilter
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')


class BlurApp(App):
    def build(self):
        Config.set('graphics', 'fullscreen', 'auto')
        self.fullscreen=True
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Enter blur radius:'))
        self.radius_input = TextInput(text='10', multiline=False)
        self.layout.add_widget(self.radius_input)
        self.button = Button(text='Blur Image', on_press=self.blur_image)
        self.layout.add_widget(self.button)
        self.img = Image(source='c:/Eye_Test.jpg')
        self.layout.add_widget(self.img)
        return self.layout

    def blur_image(self, instance):
        radius = int(self.radius_input.text)
        image = img.open('c:/Eye_Test.jpg')
        boxImage = image.filter(ImageFilter.BoxBlur(radius))
        boxImage.show()
        image = image.convert("RGBA")
        blurred = image.filter(ImageFilter.BoxBlur(radius))
        blurred_image = blurred.tobytes("raw", "RGBA", 0, -1)
        texture = Texture.create(size=(blurred.width, blurred.height))
        texture.blit_buffer(blurred_image, colorfmt='rgba', bufferfmt='ubyte')
        with self.img.canvas:
            Rectangle(texture=texture, pos=self.img.pos, size=self.img.size)


if __name__ == '__main__':
    BlurApp().run()
