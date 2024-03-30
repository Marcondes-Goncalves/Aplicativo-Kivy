
from importlib.machinery import PathFinder
from kivy.app import App

import requests

class MyFireBase():
    
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

            link = f"https://aplicativovendashash-b0c09-default-rtdb.firebaseio.com/{local_id}.json"

            info_usuario = '{"avatar": "foto1.png", "equipe": "", "total_vendas": "0", "vendas": ""}'

            requisicao_usuario = requests.patch(link, data = info_usuario)

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

        print(requisicao_dic)

    def fazer_login(self, email, senha):
        ...