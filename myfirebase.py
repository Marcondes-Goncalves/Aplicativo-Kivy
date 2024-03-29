
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