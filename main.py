
from lib2to3.pytree import type_repr
from shutil import ExecError
from sys import exception
from kivy.app import App
from kivy.lang import Builder

# API para fazer requisições
import requests

#temos que importar essa lib quando usamos request e acessamos links com https para gerar o nosso certificado de segurança
import certifi

import os
from datetime import date

# o partial permite passar um parâmetro para uma função que está sendo passado  como parametro de um botão
from functools import partial

from BannerVendedor import BannerVendedor
from myfirebase import MyFireBase
from telas import *
from botoes import *
from bannervenda import *

# certificado de segurança
# sem esse certificado não conseguimos fazer as requisições no celular
os.environ["SSL_CERT_FILE"] = certifi.where()

# No arquivo kv está escrito o nosso gerenciador de telas
GUI = Builder.load_file("main.kv")


class MainApp(App):
    """Classe padrão para criar um App
    """

    cliente = None
    produto = None
    unidade = None

    def build(self):

        # Estamos usando as funções da classe MyFireBase no loginpage.kv
        self.firebase = MyFireBase()
        return GUI

    # Essa função é executada na inicialização do aplicativo
    def on_start(self):

        # carregar as fotos de perfil e também a altera se o usuário clicar em uma
        arquivos = os.listdir("icones/fotos_perfil")
        pagina_fotoperfil = self.root.ids['fotoperfilpage'] # type: ignore[Unknown]
        lista_fotos = pagina_fotoperfil.ids['lista_fotos_perfil']
        for foto in arquivos: # o partial permite passar um parâmetro para uma função que está sendo passado  como parametro de um botão
            imagem = ImageButton(source = f'icones/fotos_perfil/{foto}', on_release = partial( self.mudar_foto_perfil, foto))
            lista_fotos.add_widget(imagem)


        # carregar as fotos dos clientes
        arquivos = os.listdir("icones/fotos_clientes")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]
        for fotoCliente in arquivos:
            imagem = ImageButton(source = f"icones/fotos_clientes/{fotoCliente}", on_release = partial(self.selecionar_cliente, fotoCliente))
            label = LabelButton(text = fotoCliente.replace(".png", "").capitalize(), on_release = partial(self.selecionar_cliente, fotoCliente))
            lista_clientes.add_widget(imagem)
            lista_clientes.add_widget(label)


        # carregar as fotos dos produtos
        arquivos = os.listdir("icones/fotos_produtos")
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]
        for fotoProduto in arquivos:
            imagem = ImageButton(source = f"icones/fotos_produtos/{fotoProduto}", on_release = partial(self.selecionar_produto, fotoProduto))
            label = LabelButton(text = fotoProduto.replace(".png", "").capitalize(), on_release = partial(self.selecionar_produto, fotoProduto))
            lista_produtos.add_widget(imagem)
            lista_produtos.add_widget(label)


        #  carregar a data
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        label_data = pagina_adicionarvendas.ids["label_data"]
        label_data.text = f"Data: {date.today().strftime('%d/%m/%Y')}"

        #carrega as infos do usuário
        self.carregar_infos_usuario()


    def carregar_infos_usuario(self):
        try:
            # Se o usuário ja tiver logado antes nós vamos pegar o seu refresh_token no arquivo de texto e vamos logalo  automaticamente assim também como vamos carregar as suas informações
            with open("refresh.txt", "r") as arquivo:
                refresh_token = arquivo.read()
            local_id, id_token = self.firebase.trocar_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            # as nossas requisições tem que terminar com .json no final do link para podermos manipular com python
            requisicao = requests.get(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}") # pegando as informaçõs do usuário
            # pegando o json e transformando em um dicionario
            requisicao_dic:dict = requisicao.json()

            # pegando o avatar da requisição por meio da chave do dicionario ['avatar']
            avatar = requisicao_dic['avatar']
            self.avatar = avatar
            # selecionando o id foto_perfil do meu arquivo main.kv
            foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
            # alterando o source com a nova foto de perfil que veio da requisição
            foto_perfil.source = f"icones/fotos_perfil/{avatar}"

            # Preencher o ID único 
            id_vendedor = requisicao_dic["id_vendedor"]
            self.id_vendedor = id_vendedor
            pagina_ajustes = self.root.ids["ajustespage"] # type: ignore[Unknown]
            pagina_ajustes.ids["idVendedor"].text=f'Seu ID Único: {id_vendedor}'

            # Preencher total de vendas
            total_vendas = requisicao_dic["total_vendas"]
            self.total_vendas = total_vendas
            home_page = self.root.ids["homepage"] # type: ignore[Unknown]
            home_page.ids["label_total_vendas"].text=f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

            # Preencher equipe
            self.equipe = requisicao_dic["equipe"]
            
            # Carregando as informações de vendas do usuário
            try: # preencher lista de vendas
                #print(requisicao_dic)
                vendas = requisicao_dic['vendas'] # retorna uma lista de dicionario que contém a informação das vendas de cada cliente
                self.vendas = vendas
                # Recuperando todos os ids da pagina homepage
                pagina_homepage = self.root.ids['homepage'] # type: ignore[Unknown]
                # Selecionando apenas o id lista_vendas
                lista_vendas = pagina_homepage.ids['lista_vendas']
                
                for id_venda in vendas:
                    venda = vendas[id_venda]
                    #print(id_venda)
                    #print(venda)
                    # Pegando as chaves e o valores de cada dicionario venda e instânciando a nossa classe
                    banner = BannerVenda(cliente = venda['cliente'], foto_cliente = venda['foto_cliente'], produto = venda['produto'],
                            foto_produto = venda['foto_produto'], data = venda['data'], preco = venda['preco'], unidade = venda['unidade'],
                            quantidade = venda['quantidade'])
                
                    # Adicionando o nosso banner a lista de vendas
                    lista_vendas.add_widget(banner)

            except Exception as e:
                print(f'Erro ao preencher banner venda: {e}')
            # Fim do Carregando as informações de vendas do usuário
            
            # Preencher equipe de vendedores
            equipe = requisicao_dic["equipe"]
            lista_equipe: list = equipe.split(",")
            pagina_lista_vendedores = self.root.ids["listarvendedorespage"] # type: ignore[Unknown]
            lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]

            for id_vendedor_equipe in lista_equipe:
                if id_vendedor_equipe != "":
                    banner_vendedor = BannerVendedor(id_vendedor = id_vendedor_equipe)
                    lista_vendedores.add_widget(banner_vendedor)
                    # Fim Preencher equipe de vendedores

            self.mudarTela("homepage")

        except Exception as a:
            print(f'Erro ao cerregar informações do usuário: {a}')


    def adicionar_vendedor(self, id_vendedor_adicionado):

        link = f'https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"&equalTo="{id_vendedor_adicionado}"'
        
        requisicao = requests.get(link)
        requisicao_dict = requisicao.json()

        pagina_adicionarvendedor = self.root.ids["adicionarvendedorpage"] # type: ignore[Unknown]
        mensagem_texto = pagina_adicionarvendedor.ids["mensagem_outrovendedor"]
       
        if requisicao_dict == {}:
            mensagem_texto.text = "Usuário não encontrado"
        else:
            equipe = self.equipe.split(",")
            if id_vendedor_adicionado in equipe:
                mensagem_texto.text = "Vendedor já faz parte da equipe"
            else:
                self.equipe = self.equipe + f",{id_vendedor_adicionado}"
                info = f'{{"equipe": "{self.equipe}"}}'
                requisicao = requests.patch(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data = info)

                mensagem_texto.text = "Vendedor adicionado com sucesso"
                # Adiciona um novo Banner a nossa lista de vendedores
                pagina_lista_vendedores = self.root.ids["listarvendedorespage"] # type: ignore[Unknown]
                lista_vendedores = pagina_lista_vendedores.ids["lista_vendedores"]

                banner_vendedor = BannerVendedor(id_vendedor = id_vendedor_adicionado)
                lista_vendedores.add_widget(banner_vendedor)


    # o Pylance não está reconhecendo o parâmetro ids, mas está funcionando.
    def mudarTela(self, idTela: str):
        """ Função para mudar de tela.

        gerenciadorTelas: self.root.ids["screen_manager"]
            gerenciadorTelas.current: idTela
        """
        # Por meio do ScreenManager que foi definido no arquivo main.kv, podemos alternar entre telas.
        # self.root é o arquivo que carregamos na nossa GUI ou seja o main.kv
        gerenciadorTelas = self.root.ids["screen_manager"] # type: ignore[Unknown]
        gerenciadorTelas.current = idTela


    def mudar_foto_perfil(self, foto, *args):
        """Função para mudar a foto de perfil do usuário

        foto:
            str: nome da foto

        *args:
            argumento padrão.
        """
        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/{foto}"

        # editaremos o campo  avatar com a nova foto
        # OBS: o dado que será passado para o banco tem que ser convertido no padrão abaixo
        info = f'{{"avatar": "{foto}"}}'

        requests.patch(f'https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}', data = info)
        
        self.mudarTela('ajustespage')


    def selecionar_cliente(self, foto, *args):

        self.cliente = foto.replace(".png", "")

        # pintar de azul o nome do item seelcionado
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        lista_clientes = pagina_adicionarvendas.ids["lista_clientes"]

        # pintando os textos que não estão selecionados de branco 
        for item in list(lista_clientes.children):
            item.color = (1,1,1,1)
            # pintar de azul o item selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255,1)
            except:
                pass


    def selecionar_produto(self, foto, *args):

        self.produto = foto.replace(".png", "")

        # pintar de azul o nome do item seelcionado
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        lista_produtos = pagina_adicionarvendas.ids["lista_produtos"]

        # pintando os textos que não estão selecionados de branco 
        for item in list(lista_produtos.children):
            item.color = (1,1,1,1)
            # pintar de azul o item selecionado
            try:
                texto = item.text
                texto = texto.lower() + ".png"
                if foto == texto:
                    item.color = (0, 207/255, 219/255,1)
            except:
                pass


    def selecionar_unidadade(self, id_label, *args):
        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]

        self.unidade = id_label.replace("unidades_", "")

        #pintar todos de branco
        pagina_adicionarvendas.ids["unidades_kg"].color = (1,1,1,1)
        pagina_adicionarvendas.ids["unidades_unidades"].color = (1,1,1,1)
        pagina_adicionarvendas.ids["unidades_litros"].color = (1,1,1,1)

        #pintar o selecionado de azul
        pagina_adicionarvendas.ids[id_label].color = (0, 207/255, 219/255,1)


    def adicionar_venda(self):
        cliente = self.cliente
        produto = self.produto
        unidade = self.unidade

        pagina_adicionarvendas = self.root.ids["adicionarvendaspage"] # type: ignore[Unknown]
        data = pagina_adicionarvendas.ids["label_data"].text.replace("Data: ", "")

        preco = pagina_adicionarvendas.ids["preco_total"].text
        quantidade = pagina_adicionarvendas.ids["quantidade"].text

        # Se esses campos não forem selecionados os mesmo serão pintados de vermelho!
        if not cliente:
            pagina_adicionarvendas.ids["label_selecione_cliente"].color = (1,0,0,1)

        if not produto:
            pagina_adicionarvendas.ids["label_selecione_produto"].color = (1,0,0,1)

        if not unidade:
            pagina_adicionarvendas.ids["unidades_kg"].color = (1,0,0,1)
            pagina_adicionarvendas.ids["unidades_unidades"].color = (1,0,0,1)
            pagina_adicionarvendas.ids["unidades_litros"].color = (1,0,0,1)
            
        if not preco:
            pagina_adicionarvendas.ids["label_preco"].color = (1,0,0,1)
        else:
            try:
                preco = float(preco)
            except:
                pagina_adicionarvendas.ids["label_preco"].color = (1,0,0,1)

        if not quantidade:
            pagina_adicionarvendas.ids["label_quantidade"].color = (1,0,0,1)
        else:
            try:
                quantidade = float(quantidade)
            except:
                pagina_adicionarvendas.ids["label_quantidade"].color = (1,0,0,1)

        # Se ele preencheu tudo vamos enviar os dados
        if cliente and produto and unidade and preco and quantidade and type(preco) == float and type(quantidade) == float:
            foto_produto = produto + ".png"
            foto_cliente = cliente + ".png" 

            info = f'{{"cliente": "{cliente}", "produto": "{produto}", "foto_cliente": "{foto_cliente}", "foto_produto": "{foto_produto}", "data": "{data}", "unidade": "{unidade}", "preco": "{preco}", "quantidade": "{quantidade}"}}'

            requests.post(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}/vendas.json?auth={self.id_token}", data = info)

            banner = BannerVenda(cliente = cliente, produto = produto, foto_cliente = foto_cliente, foto_produto = foto_produto, data = data, unidade = unidade, preco = preco, quantidade = quantidade)

            # Recuperando todos os ids da pagina homepage
            pagina_homepage = self.root.ids['homepage'] # type: ignore[Unknown]
            # Selecionando apenas o id lista_vendas
            lista_vendas = pagina_homepage.ids['lista_vendas']
            lista_vendas.add_widget(banner)

            # pegando o total de vendas e atualizando o seu valor
            requisicao = requests.get(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}/total_vendas.json?auth={self.id_token}")
            total_vendas = float(requisicao.json())
            total_vendas += preco

            # atualizando o total de vendas no banco
            info = f'{{"total_vendas": "{total_vendas}"}}'
            requests.patch(f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{self.local_id}.json?auth={self.id_token}", data = info)

            # atualizando o total de vendas na home page
            home_page = self.root.ids["homepage"] # type: ignore[Unknown]
            home_page.ids["label_total_vendas"].text=f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

            self.mudarTela("homepage")

        self.cliente = None
        self.produto = None
        self.unidade = None
        

    def carregar_todas_vendas(self):
        pagina_todasvendaspage = self.root.ids["todasvendaspage"] # type: ignore[Unknown]
        lista_todas_vendas = pagina_todasvendaspage.ids["lista_vendas"]

        for item in list(lista_todas_vendas.children):
            lista_todas_vendas.remove_widget(item)



        #Preencher a página todasvendaspage
        # as nossas requisições tem que terminar com .json no final do link para podermos manipular com python
        # pegando as informaçõs da empresa
        requisicao = requests.get(f'https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/.json?orderBy="id_vendedor"') 
        # pegando o json e transformando em um dicionario
        requisicao_dic:dict = requisicao.json()
        #print(requisicao_dic)

        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/hash.png"

        total_vendas: float = 0

        for local_id_usuario in requisicao_dic:
            try:
                vendas = requisicao_dic[local_id_usuario]["vendas"]

                for id_venda in vendas:
                    venda = vendas[id_venda]

                    total_vendas += float(venda["preco"])

                    banner = BannerVenda(cliente = venda['cliente'], foto_cliente = venda['foto_cliente'], produto = venda['produto'],
                            foto_produto = venda['foto_produto'], data = venda['data'], preco = venda['preco'], unidade = venda['unidade'],
                            quantidade = venda['quantidade'])
                    
                    lista_todas_vendas.add_widget(banner)
                    
            except :
                pass
            
        # Preencher total de vendas
        pagina_todasvendaspage.ids["label_total_vendas"].text=f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]'

        # Redirecionar para a página todasvendaspage
        self.mudarTela("todasvendaspage")


    def sair_todas_vendas(self, id_tela):
        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        
        # alterando o source com a nova foto de perfil que veio da requisição
        foto_perfil.source = f"icones/fotos_perfil/{self.avatar}"

        self.mudarTela(id_tela)


    def carregar_vendas_vendedor(self, dic_info_vendedor, *args):

        try:
            vendas = dic_info_vendedor["vendas"]

            pagina_vendasoutrovendedor = self.root.ids["vendasoutrovendedorpage"] # type: ignore[Unknown]
            lista_vendas = pagina_vendasoutrovendedor.ids["lista_vendas"]

            # limpando as vendas para garantir que não tenha vendas duplicadas
            for item in list(lista_vendas.children):
                lista_vendas.remove_widget(item)

            for id_venda in vendas:
                venda = vendas[id_venda]

                banner = BannerVenda(cliente = venda['cliente'], foto_cliente = venda['foto_cliente'], produto = venda['produto'],
                        foto_produto = venda['foto_produto'], data = venda['data'], preco = venda['preco'], unidade = venda['unidade'],
                        quantidade = venda['quantidade'])
                    
                lista_vendas.add_widget(banner)
        except :
            pass

        total_vendas = dic_info_vendedor["total_vendas"]
        # Preencher total de vendas
        pagina_vendasoutrovendedor.ids["label_total_vendas"].text=f'[color=#000000]Total de Vendas:[/color] [b]R${total_vendas}[/b]' # type: ignore[Unknown]

        # selecionando o id foto_perfil do meu arquivo main.kv
        foto_perfil = self.root.ids["foto_perfil"] # type: ignore[Unknown]
        # alterando o source com a nova foto de perfil que veio da requisição
        avatar = dic_info_vendedor['avatar']
        foto_perfil.source = f"icones/fotos_perfil/{avatar}"

        self.mudarTela("vendasoutrovendedorpage")


MainApp().run()

