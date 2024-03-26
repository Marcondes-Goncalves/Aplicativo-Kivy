
from kivy.app import App
from kivy.lang import Builder

from telas import *
from botoes import *

# API para fazer requisições
import requests

# No arquivo kv está escrito o nosso gerenciador de telas
GUI = Builder.load_file("main.kv")


class MainApp(App):
    """Classe padrão para criar um App
    """
    id_usuario = 1

    def build(self):
        return GUI

    # Essa função é executada na inicialização do aplicativo
    def on_start(self):

        # as nossas requisições tem que terminar com .json no final do link para podermos manipular com python
        requisicao = requests.get(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.id_usuario}.json") # pegando as informaçõs do usuário
        # pegando o json e transformando em um dicionario
        requisicao_dic = requisicao.json()

        try: # preencher lista de vendas
            vendas = requisicao_dic['vendas'][1:] # pegando as vendas da lista de vendas que tenha uma ou mais vendas 
            for venda in vendas:
                print(venda)
        except:
            pass


        # pegando o avatar da requisição por meio da chave do dicionario ['avatar']
        avatar = requisicao_dic['avatar']
        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"]
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"


    # o Pylance não está reconhecendo o parâmetro ids, mas está funcionando.
    def mudarTela(self, idTela: str):
        # Essa função recebe o id da tela para mudar de tela.
  
        # Por meio do ScreenManager que foi definido no arquivo main.kv, podemos alternar entre telas.
        # self.root é o arquivo que carregamos na nossa GUI ou seja o main.kv
        gerenciadorTelas = self.root.ids["screen_manager"]
        gerenciadorTelas.current = idTela


MainApp().run()
