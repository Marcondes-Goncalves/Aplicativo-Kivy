
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

class HomePage(Screen):
    pass



# No arquivo kv está escrito a nossa interface
GUI = Builder.load_file("main.kv")
class MainApp(App):

    def build(self):
        return GUI

    def on_start(self):
        pass

MainApp().run()

