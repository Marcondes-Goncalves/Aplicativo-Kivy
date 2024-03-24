
from kivy.app import App
from kivy.lang import Builder

# No arquivo kv está escrito a nossa interface
GUI = Builder.load_file("main.kv")

class MainApp(App):

    def build(self):
        return GUI




MainApp().run()

