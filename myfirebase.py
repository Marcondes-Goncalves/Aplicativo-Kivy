
import requests

class MyFireBase():
    
    API_KEY: str = "AIzaSyATe004SXsbO8gXFLbWbaxQnv_E1207JbQ"



    def criar_conta(self, email, senha):

        link = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.API_KEY}"

        info = {"email":email, "senha": senha, "returnSecureToken": True}

        requisicao = requests.post(link, data = info)
        
        requisicao_dic = requisicao.json()

        print(requisicao_dic)

    def fazer_login(self, email, senha):
        ...