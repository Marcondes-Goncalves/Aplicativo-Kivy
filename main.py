
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
        # ScreenManager é um gerenciador de telas e por meio dele podemos alternar entre telas
        gerenciadorTelas = self.root.ids["screen_manager"] # Por meio do ScreenManager que foi definido no arquivo main.kv, podemos alternar entre telas.
        gerenciadorTelas.current = idTela



MainApp().run()
