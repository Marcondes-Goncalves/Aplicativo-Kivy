from cgitb import text
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App

# o partial permite passar um parâmetro para uma função que está sendo passado  como parametro de um botão
from functools import partial

from botoes import ImageButton, LabelButton

import requests

class BannerVendedor(FloatLayout):
    
    def __init__(self, **kwargs):
        super().__init__()

        
        # escrevendo o nosso fundo do ScrollView 
        with self.canvas: # type: ignore[Unknown]
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size = self.size, pos = self.pos)
        self.bind(pos = self.atualizar_rec, size = self.atualizar_rec) # # type: ignore[Unknown]
        # bind é responsalvel por atualizar o nosso Rectangle uma vez que o usuário altera o tamanho da tela


        id_vendedor = kwargs["id_vendedor"]

        link = f'https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor}"'

        requisicao = requests.get(link)
        requisicao_dict = requisicao.json()
        valor = list(requisicao_dict.values())[0]
        avatar = valor["avatar"]
        total_vendas =valor["total_vendas"]
        #print(valor)

        meu_aplicativo = App.get_running_app()

        imagem = ImageButton(source = f"icones/fotos_perfil/{avatar}", pos_hint={'right': 0.4, 'top': 0.9}, size_hint=(0.3, 0.8), 
                             on_release = partial(meu_aplicativo.carregar_vendas_vendedor, valor)) # type: ignore[Unknown]
        
        label_id = LabelButton(text = f"ID vendedor: {id_vendedor}", pos_hint={'right': 0.9, 'top': 0.9}, size_hint=(0.5, 0.5), 
                               on_release = partial(meu_aplicativo.carregar_vendas_vendedor, valor)) # type: ignore[Unknown]
        
        label_total = LabelButton(text= f"Total de vendas: R${total_vendas}", pos_hint={'right': 0.9, 'top': 0.6}, size_hint=(0.5, 0.5), 
                                  on_release = partial(meu_aplicativo.carregar_vendas_vendedor, valor)) # type: ignore[Unknown]

        self.add_widget(imagem)
        self.add_widget(label_id)
        self.add_widget(label_total)

    # Função que atualiza o retangulo quando o usuario altera o tamanho da tela
    def atualizar_rec(self, *args):
        self.rec.pos  = self.pos
        #print('atualizou o self.rec.pos')
        self.rec.size = self.size
        #print('atualizou o self.rec.size')
