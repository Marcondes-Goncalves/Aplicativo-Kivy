
from cgitb import text
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

# Widget personalizado que vamos utilizar em nosso banner

class BannerVenda(GridLayout): # Por padrão a nossa classe será um GridLayout
    

    # **kwargs significa que eu vou passar um dicionario com varios itens. Poderiamos também fazer da forma tradicional, mas dessa forma é mais simples. 
    def __init__(self, **kwargs): # EXEMPLO: kwargs vai ser igual a {'cliente': 'mundial', 'foto_cliente': 'marcondes.png'}
        self.rows = 1 # LEMBRETE: temos que adicionar a quantidade de linhas a todo GridLayout a não ser que ele esteja dentro de um ScrollView
        super().__init__() # Herdando todas as propriedades do GridLayout


        # escrevendo o nosso fundo do ScrollView 
        with self.canvas: # type: ignore[Unknown]
            Color(rgb=(0, 0, 0, 1))
            self.rec = Rectangle(size = self.size, pos = self.pos)
        self.bind(pos = self.atualizar_rec, size = self.atualizar_rec) # # type: ignore[Unknown]
        # bind é responsalvel por atualizar o nosso Rectangle uma vez que o usuário altera o tamanho da tela

        # pegando os valores por meio da chave do dicionario que foi passado para o nosso construtor __init__
        cliente      = kwargs['cliente'     ]
        foto_cliente = kwargs['foto_cliente']
        produto      = kwargs['produto'     ]
        foto_produto = kwargs['foto_produto']
        data         = kwargs['data'        ]
        unidade      = kwargs['unidade'     ]
        quantidade   = kwargs['quantidade'  ]
        preco        = kwargs['preco'       ]


        esquerda        = FloatLayout()
        esquerda_imagem = Image(pos_hint = {'right': 1, 'top': 0.95}, size_hint = ( 1, 0.75), source = f"icones/fotos_clientes/{foto_cliente}")
        esquerda_label  = Label(text = cliente, size_hint=(1, 0.2), pos_hint={'right': 1, 'top': 0.2})
        esquerda.add_widget(esquerda_imagem)
        esquerda.add_widget(esquerda_label )


        meio        = FloatLayout()
        meio_imagem = Image(pos_hint = {'right': 1, 'top': 0.95}, size_hint = ( 1, 0.75), source = f"icones/fotos_produtos/{foto_produto}")
        meio_label  = Label(text = produto, size_hint = (1, 0.2), pos_hint = {'right': 1, 'top': 0.2})
        meio.add_widget(meio_imagem)
        meio.add_widget(meio_label )


        direita                   = FloatLayout() 
        direita_label_data        = Label(text = f"Data: {data}", size_hint=(1, 0.33), pos_hint={'right': 1, 'top': 0.9})
        direita_label_preco       = Label(text = f"Preço: R${preco:,.2f}", size_hint=(1, 0.33), pos_hint={'right': 1, 'top': 0.65})
        direita_label_quantidade  = Label(text = f"{quantidade} {unidade}", size_hint = (1, 0.33), pos_hint = {'right': 1, 'top': 0.4})
        direita.add_widget(direita_label_data      )
        direita.add_widget(direita_label_preco     )
        direita.add_widget(direita_label_quantidade)


        # Aqui estamos referenciando a nossa própria classe e adicionando 3 FloatLayout a ela,
        self.add_widget(esquerda)
        self.add_widget(meio    )
        self.add_widget(direita )


    # Função que atualiza o retangulo quando o usuario altera o tamanho da tela
    def atualizar_rec(self, *args):
        self.rec.pos  = self.pos
        #print('atualizou o self.rec.pos')
        self.rec.size = self.size
        #print('atualizou o self.rec.size')
