import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.graphics.texture import Texture
from kivy.clock import Clock

Clock.schedule_interval(lambda dt: None, 0)
import traceback


class BlurApp(App):
    def build(self):

        # Create main layout
        self.layout = BoxLayout(orientation='vertical')

        # Create box layout for the image and the controls
        self.image_layout = BoxLayout(size_hint=(1, 0.9))
        self.control_layout = BoxLayout(size_hint=(1, 0.1), spacing=10, padding=10)

        # Add the image widget to the image layout
        self.img = Image()
        self.image_layout.add_widget(self.img)

        # Add the image layout and the control layout to the main layout
        self.layout.add_widget(self.image_layout)
        self.layout.add_widget(self.control_layout)

        # Create label and slider for blur radius
        self.control_layout.add_widget(Label(text='Blur Radius:'))
        self.radius_slider = Slider(min=1, max=51, step=2, value=11, size_hint=(0.5, 1))
        self.radius_slider.bind(value=self.blur_image)
        self.control_layout.add_widget(self.radius_slider)

        # Create button to open camera
        self.camera_button = Button(text='Open Camera', size_hint=(0.2, 1), on_press=self.camera)
        self.control_layout.add_widget(self.camera_button)

        return self.layout

    def blur_image(self, instance, value):
        radius = int(value)

        # Load image and apply blur
        img = cv2.imread('c://Projects//Eye-Test-App//Eye_Test.jpg')
        img = cv2.flip(img, 0)
        blurred = cv2.GaussianBlur(img, (radius, radius), 0)

        # Convert the blurred image to a texture
        blurred_image = blurred.tobytes()
        texture = Texture.create(size=(blurred.shape[1], blurred.shape[0]), colorfmt='bgr')
        texture.blit_buffer(blurred_image, colorfmt='bgr', bufferfmt='ubyte')

        # Update the image widget with the blurred image
        self.img.texture = texture

    def blur_image(self, instance, value):
        radius = int(value)

        if self.camera_button.text == 'Close Camera':
            # If camera is open, get the current frame and apply blur
            ret, frame = self.cap.read()
            if ret:
                # Flip the frame
                frame = cv2.flip(frame, 0)
                blurred = cv2.GaussianBlur(frame, (radius, radius), 0)

                # Convert the blurred image to a texture
                blurred_image = blurred.tobytes()
                texture = Texture.create(size=(blurred.shape[1], blurred.shape[0]), colorfmt='bgr')
                texture.blit_buffer(blurred_image, colorfmt='bgr', bufferfmt='ubyte')

                # Update the image widget with the blurred image
                self.img.texture = texture
        else:
            # If camera is not open, load the image and apply blur
            img = cv2.imread('c://Projects//Eye-Test-App//Eye_Test.jpg')
            img = cv2.flip(img, 0)
            blurred = cv2.GaussianBlur(img, (radius, radius), 0)

            # Convert the blurred image to a texture
            blurred_image = blurred.tobytes()
            texture = Texture.create(size=(blurred.shape[1], blurred.shape[0]), colorfmt='bgr')
            texture.blit_buffer(blurred_image, colorfmt='bgr', bufferfmt='ubyte')

            # Update the image widget with the blurred image
            self.img.texture = texture

    def camera(self, instance):
        # Open the default camera
        cap = cv2.VideoCapture(0)

        # Check if camera was successfully opened
        if not cap.isOpened():
            print("Error opening camera")
            return

        # Create a Clock object to schedule the video frame updates
        self.video_clock = Clock.schedule_interval(lambda dt: self.update_video(cap), 1.0/30.0)

    def update_video(self, cap):
        # Capture frame-by-frame
        ret, frame = cap.read()

        if ret:
            frame = cv2.flip(frame, 0)
            # Apply Gaussian blur filter to the frame
            radius = int(self.radius_slider.value)
            blurred = cv2.GaussianBlur(frame, (radius, radius), 0)

            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB)

            # Convert the frame to texture
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(rgb_frame.flatten(), colorfmt='rgb', bufferfmt='ubyte')

            # Update the image widget with the blurred image
            self.img.texture = texture

    def on_stop(self):
        # Stop the video clock when the app is closed
        self.video_clock.cancel()


if __name__ == '__main__':
    BlurApp().run()
