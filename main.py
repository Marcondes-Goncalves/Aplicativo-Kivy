
from sys import exception
from kivy.app import App
from kivy.lang import Builder

# API para fazer requisições
import requests

import os

# o partial permite passar um parâmetro para uma função que está sendo passado  como parametro de um botão
from functools import partial

from myfirebase import MyFireBase
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

        # Estamos usando as funções da classe MyFireBase no loginpage.kv
        self.firebase = MyFireBase()

        return GUI

    # Essa função é executada na inicialização do aplicativo
    def on_start(self):

        # carregar as fotos de perfil
        arquivos = os.listdir("icones/fotos_perfil")

        pagina_fotoperfil = self.root.ids['fotoperfilpage'] # type: ignore[Unknown]
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']

        for foto in arquivos: # o partial permite passar um parâmetro para uma função que está sendo passado  como parametro de um botão
            imagem = ImageButton(source = f'icones/fotos_perfil/{foto}', on_release = partial( self.mudar_foto_perfil, foto))

            lista_fotos.add_widget(imagem)


        #carrega as infos do usuário
        self.carregar_infos_usuario()


    def carregar_infos_usuario(self):
        # as nossas requisições tem que terminar com .json no final do link para podermos manipular com python
        requisicao = requests.get(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.id_usuario}.json") # pegando as informaçõs do usuário
        # pegando o json e transformando em um dicionario
        requisicao_dic:dict = requisicao.json()

        # pegando o avatar da requisição por meio da chave do dicionario ['avatar']
        avatar = requisicao_dic['avatar']
        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        try: # preencher lista de vendas
            vendas = requisicao_dic['vendas'][1:] # retorna uma lista de dicionario que contém a informação das vendas de cada cliente

            # Recuperando todos os ids da pagina homepage
            pagina_homepage = self.root.ids['homepage'] # type: ignore[Unknown]
            # Selecionando apenas o id lista_vendas
            lista_vendas = pagina_homepage.ids['lista_vendas']
            
            for venda in vendas:
                # Pegando as chaves e o valores de cada dicionario venda e instânciando a nossa classe
                banner = BannerVenda(cliente = venda['cliente'], foto_cliente = venda['foto_cliente'], produto = venda['produto'],
                         foto_produto = venda['foto_produto'], data = venda['data'], preco = venda['preco'], unidade = venda['unidade'],
                         quantidade = venda['quantidade'])
            
                # Adicionando o nosso banner a lista de vendas
                lista_vendas.add_widget(banner)

        except Exception as e:
            print(f'Erro: {e}')


    # o Pylance não está reconhecendo o parâmetro ids, mas está funcionando.
    def mudarTela(self, idTela: str):
        # Essa função recebe o id da tela para mudar de tela.
        # Por meio do ScreenManager que foi definido no arquivo main.kv, podemos alternar entre telas.
        # self.root é o arquivo que carregamos na nossa GUI ou seja o main.kv
        gerenciadorTelas = self.root.ids["screen_manager"] # type: ignore[Unknown]
        gerenciadorTelas.current = idTela


    def mudar_foto_perfil(self, foto, *args):
        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        # editaremos o campo  avatar com a nova foto
        # OBS: o dado que será passado para o banco tem que ser convertido no padrão abaixo
        info = f'{{"avatar": "{foto}"}}'

        requests.patch(f'https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.id_usuario}.json', 
                                    data = info)
        
        self.mudarTela('ajustespage')


MainApp().run()

