from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser

Builder.load_file('frontend.kv')

class CameraScreen(Screen): # This class can replace Webcam Class
    # This class represents both Webcam and CameraScreen (Kivy)

    def start(self):
        """Starts the Camera and changes Button text"""
        self.ids.camera.play = True
        self.ids.camera.opacity = 1
        # self.ids.camera_button.text = "Stop Camera"
        # self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops the Camera and changes Button text"""
        self.ids.camera.play = False
        # self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        """Creates a filename with the current time, captures
        and saves a photo image under that filename"""
        if self.ids.camera.play == True:
            current_time = time.strftime('%Y%m%d-%H%M%S')
            self.filepath = f'Images/image_{current_time}.png'
            self.ids.camera.export_to_png(self.filepath)
            self.manager.current = 'image_screen' # The name of the
            # second Screen in the Kivy File
            self.manager.current_screen.ids.img.source = self.filepath

            # self.ids = Gives us access on the widgets of the class where the
            # code is written.
            # self.manager.current_screen.ids:
            # will give us access to the widgets of the current screen
            # that the user is using
        else:
            pass

from filestack import Client

class FileSharer:

    def __init__(self, filepath, api_key='A5UGt0qSwQN2Z6fsFfZ5Tz'):
        # create a free account on filestack.com and copy your API
        # and replace my API with yours
        self.filepath = filepath
        self.api_key = api_key

    def share(self):
        client = Client(self.api_key)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url

class ImageScreen(Screen):

    link_message = "Generate the link first please!"
    def create_link(self):
        """The method accesses the photo filepath, uploads it to the web,
        and inserts the link in the label widget"""
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        sharer = FileSharer(filepath=file_path)
        self.url = sharer.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copies the link to the clipboard and makes it
        available to posting"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Opens the link with the default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message

class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
        return RootWidget()

MainApp().run()