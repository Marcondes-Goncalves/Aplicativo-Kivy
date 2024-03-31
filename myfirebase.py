
from importlib.machinery import PathFinder
from kivy.app import App

import requests

class MyFireBase():
    """Classe para gerênciar o login e criar uma nova conta do usuário
    """
    
    API_KEY: str = "AIzaSyATe004SXsbO8gXFLbWbaxQnv_E1207JbQ"



    def criar_conta(self, email, senha):

        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email":email, "password": senha, "returnSecureToken": True}

        requisicao = requests.post(link, data = info)
        
        requisicao_dic = requisicao.json()

        if requisicao.ok:
            print("Usuário criado")

            refresh_token = requisicao_dic['refreshToken'] # -> token mantém o usuário logado
            local_id = requisicao_dic['localId'] # -> id do usuário
            id_token = requisicao_dic['idToken'] # -> autenticação

            # Pegando a instância do meu aplicativo em execução
            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id # type: ignore[Unknown]
            meu_aplicativo.id_token = id_token # type: ignore[Unknown]

            # Salvando o token do usuário em um arquivo txt, para que da próxima vez que ele entrar no aplicativo, o mesmo não precise logar novamente.
            with open("refresh.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            # Pegando o id do próximo vendedor
            req_id = requests.get("https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/proximo_id_vendedor.json")
            id_vendedor = req_id.json()
            #print(id_vendedor)

            # Criando o novo vendedor
            link = f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{local_id}.json"
            info_usuario = f'{{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": "", "id_vendedor": "{id_vendedor}"}}'
            requisicao_usuario = requests.patch(link, data = info_usuario)

            # atualizar o id do proximo_id_vendedor
            proximo_id_vendedor = int(id_vendedor) + 1
            info_id_vendedor = f'{{"proximo_id_vendedor": "{proximo_id_vendedor}"}}'
            requests.patch("https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/.json", data = info_id_vendedor)

            meu_aplicativo.carregar_infos_usuario() # type: ignore[Unknown]
            meu_aplicativo.mudarTela("homepage") # type: ignore[Unknown]

        else:
            # Pegando o erro e mensagem de erro da minha requisição
            mensagem_erro = requisicao_dic["error"]['message']

            # Pegando a instância do meu aplicativo em execução
            meu_aplicativo = App.get_running_app()

            # Acesando a página de login por meio da instância do aplciativo que está em execução
            pagina_login = meu_aplicativo.root.ids["loginpage"] # type: ignore[Unknown]

            # Atribuindo a mensagem de erro a minha label de id mensagem_login, da pagina loginpage.
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

        print(requisicao_dic)

    def fazer_login(self, email, senha):
        
        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.API_KEY}"

        info = {"email":email, "password": senha, "returnSecureToken": True}
        requisicao = requests.post(link, data = info)
        requisicao_dic = requisicao.json()

        if requisicao.ok:

            refresh_token = requisicao_dic['refreshToken'] # -> token mantém o usuário logado
            local_id = requisicao_dic['localId'] # -> id do usuário
            id_token = requisicao_dic['idToken'] # -> autenticação

            # Pegando a instância do meu aplicativo em execução
            meu_aplicativo = App.get_running_app()
            meu_aplicativo.local_id = local_id # type: ignore[Unknown]
            meu_aplicativo.id_token = id_token # type: ignore[Unknown]

            # Salvando o token do usuário em um arquivo txt, para que da próxima vez que ele entrar no aplicativo, o mesmo não precise logar novamente.
            with open("refresh.txt", "w") as arquivo:
                arquivo.write(refresh_token)

            meu_aplicativo.carregar_infos_usuario() # type: ignore[Unknown]

            meu_aplicativo.mudarTela("homepage") # type: ignore[Unknown]

        else:
            # Pegando o erro e mensagem de erro da minha requisição
            mensagem_erro = requisicao_dic["error"]["message"]

            # Pegando a instância do meu aplicativo em execução
            meu_aplicativo = App.get_running_app()

            # Acesando a página de login por meio da instância do aplciativo que está em execução
            pagina_login = meu_aplicativo.root.ids["loginpage"] # type: ignore[Unknown]

            # Atribuindo a mensagem de erro a minha label de id mensagem_login, da pagina loginpage.
            pagina_login.ids["mensagem_login"].text = mensagem_erro
            pagina_login.ids["mensagem_login"].color = (1, 0, 0, 1)

    def trocar_token(self, refresh_token):
        """Função para logar o usuário automáticamente se o mesmo ja tiver criado uma conta

        Args:
            refresh_token (_type_): _description_

        Returns:
            tupla: (local_id, id_token)
        """

        link = f"https://securetoken.googleapis.com/v1/token?key={self.API_KEY}"

        info = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        requisicao = requests.post(link, data = info) 

        requisicao_dic = requisicao.json()

        local_id = requisicao_dic["user_id"]
        id_token = requisicao_dic["id_token"]

        #print(requisicao_dic)
        
        return (local_id, id_token)
    
