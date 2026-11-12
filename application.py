from app.controllers.datarecord import DataRecord
from bottle import template, redirect, request, response


class Application():

    def __init__(self):

        self.pages = {
            'portal': self.portal,
            'banco': self.banco
        }

        self.__model = DataRecord()


    def render(self, page, parameter=None):
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def get_session_id(self):
        return request.get_cookie('session_id')


    def helper(self):
        return template('app/views/html/helper')


    # ------------------------- recurso PORTAL -------------------------

    def portal(self):
        return template('app/views/html/portal')


    def is_authenticated(self):
        session_id = self.get_session_id()
        return self.__model.getUserName(session_id) is not None


    def authenticate_user(self, username, password):
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            return session_id, username
        return None, None


    def logout_user(self):
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)


    # ------------------------- recurso BANCO -------------------------

    # READ: feito no próprio sistema (página /banco)
    def banco(self):
        if not self.is_authenticated():
            redirect('/portal')
        user = self.__model.getCurrentUser(self.get_session_id())
        filmes = self.__model.getFilmes()
        return template('app/views/html/banco', current_user=user, filmes=filmes)


    # CREATE: via cURL
    def create_filme(self, titulo, diretor, ano):
        if not self.is_authenticated():
            response.status = 401
            return 'Acesso negado: faça login em /portal\n'
        if not titulo or not diretor or not ano or not ano.isdigit():
            response.status = 400
            return 'Informe titulo, diretor e ano (numero)\n'
        filme = self.__model.addFilme(titulo, diretor, ano)
        response.status = 201
        return f'Filme cadastrado: id={filme.id} | {filme.titulo} | {filme.diretor} | {filme.ano}\n'


    # UPDATE: via cURL
    def update_filme(self, id, titulo, diretor, ano):
        if not self.is_authenticated():
            response.status = 401
            return 'Acesso negado: faça login em /portal\n'
        if ano and not ano.isdigit():
            response.status = 400
            return 'O ano deve ser um numero\n'
        filme = self.__model.updateFilme(id, titulo, diretor, ano)
        if not filme:
            response.status = 404
            return f'Filme {id} nao encontrado\n'
        return f'Filme atualizado: id={filme.id} | {filme.titulo} | {filme.diretor} | {filme.ano}\n'


    # DELETE: via cURL
    def delete_filme(self, id):
        if not self.is_authenticated():
            response.status = 401
            return 'Acesso negado: faça login em /portal\n'
        if self.__model.deleteFilme(id):
            return f'Filme {id} removido\n'
        response.status = 404
        return f'Filme {id} nao encontrado\n'
