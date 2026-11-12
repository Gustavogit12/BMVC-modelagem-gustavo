from app.models.user_account import UserAccount
from app.models.filme import Filme
import json
import uuid


class DataRecord():
    """Banco de dados JSON para os recursos Usuários e Filmes"""

    def __init__(self):

        self.__user_accounts = []
        self.__authenticated_users = {}
        self.__filmes = []
        self.read()


    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '000000'))

        try:
            with open("app/controllers/db/filmes.json", "r") as arquivo_json:
                filme_data = json.load(arquivo_json)
                self.__filmes = [Filme(**data) for data in filme_data]
        except FileNotFoundError:
            self.__filmes = []


    # ------------------------- Usuários (portal) -------------------------

    def getCurrentUser(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getUserName(self, session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None


    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id]  # Remove o usuário logado


    # ------------------------- Filmes (banco) -------------------------

    def getFilmes(self):
        return self.__filmes


    def getFilme(self, id):
        for filme in self.__filmes:
            if filme.id == id:
                return filme
        return None


    def addFilme(self, titulo, diretor, ano):
        novo_id = max([filme.id for filme in self.__filmes], default=0) + 1
        filme = Filme(novo_id, titulo, diretor, int(ano))
        self.__filmes.append(filme)
        self.save()
        return filme


    def updateFilme(self, id, titulo=None, diretor=None, ano=None):
        filme = self.getFilme(id)
        if not filme:
            return None
        if titulo:
            filme.titulo = titulo
        if diretor:
            filme.diretor = diretor
        if ano:
            filme.ano = int(ano)
        self.save()
        return filme


    def deleteFilme(self, id):
        filme = self.getFilme(id)
        if not filme:
            return False
        self.__filmes.remove(filme)
        self.save()
        return True


    def save(self):
        with open("app/controllers/db/filmes.json", "w") as arquivo_json:
            filme_data = [vars(filme) for filme in self.__filmes]
            json.dump(filme_data, arquivo_json, indent=4, ensure_ascii=False)
