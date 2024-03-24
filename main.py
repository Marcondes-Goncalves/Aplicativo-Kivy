
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

class HomePage(Screen):
    pass

class AjustesPage(Screen):
    pass


# No arquivo kv está escrito a nossa interface
GUI = Builder.load_file("main.kv")
class MainApp(App):

    def build(self):
        return GUI

    def on_start(self):
        pass

    # o Pylance não está reconhecendo o parâmetro ids, mas está funcionando.
    def mudarTela(self, idTela):
        gerenciadorTelas = self.root.ids["screen_manager"]
        gerenciadorTelas.current = idTela

MainApp().run()

