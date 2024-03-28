
from sys import exception
from kivy.app import App
from kivy.lang import Builder

# API para fazer requisições
import requests

from telas import *
from botoes import *
from bannervenda import *


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
            vendas = requisicao_dic['vendas'][1:] # retorna uma lista de dicionario que contém a informação das vendas de cada cliente
            # print(f'Vendas: {vendas}')
            # print('\n')
            for venda in vendas:
                # Pegando as chaves e o valores de cada dicionario venda e instânciando a nossa classe
                banner = BannerVenda(cliente = venda['cliente'], foto_cliente = venda['foto_cliente'], produto = venda['produto'],
                         foto_produto = venda['foto_produto'], data = venda['data'], preco = venda['preco'], unidade = venda['unidade'],
                         quantidade = venda['quantidade'])
                
                # Recuperando todos os ids da pagina homepage
                pagina_homepage = self.root.ids['homepage']
                # Selecionando apenas o id lista_vendas
                lista_vendas = pagina_homepage.ids['lista_vendas']
                # Adicionando o nosso banner a lista de vendas
                lista_vendas.add_widget(banner)

                # print(f'Venda: {venda}')
                # print('\n')

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
