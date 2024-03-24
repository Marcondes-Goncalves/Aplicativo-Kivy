
from kivy.app import App
from kivy.lang import Builder
from telas import *
from botoes import *

# No arquivo kv está escrito o nosso gerenciador de telas
GUI = Builder.load_file("main.kv")

class MainApp(App):
    """Classe padrão para criar um App
    """
    def build(self):
        return GUI

    def on_start(self):
        pass

    # o Pylance não está reconhecendo o parâmetro ids, mas está funcionando.
    def mudarTela(self, idTela: str):
        """Função para mudar de tela

        Parâmetro:
            Essa função recebe o id da tela para mudar de tela.
        """
        gerenciadorTelas = self.root.ids["screen_manager"]
        gerenciadorTelas.current = idTela



MainApp().run()
