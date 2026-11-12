from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')


#-----------------------------------------------------------------------------
# Suas rotas aqui:

# Recurso PORTAL (login de usuários - modelo UserAccount)

@app.route('/portal', method='GET')
def login():
    return ctl.render('portal')


@app.route('/portal', method='POST')
def action_portal():
    username = request.forms.get('username')
    password = request.forms.get('password')
    session_id, username = ctl.authenticate_user(username, password)
    if session_id:
        response.set_cookie('session_id', session_id, httponly=True, max_age=3600)
        redirect('/banco')
    else:
        return redirect('/portal')


@app.route('/logout', method='POST')
def logout():
    ctl.logout_user()
    response.delete_cookie('session_id')
    redirect('/portal')


# Recurso BANCO (lista de filmes - modelo Filme)
#   GET    /banco        -> READ   (no próprio sistema)
#   POST   /banco        -> CREATE (cURL)
#   PUT    /banco/<id>   -> UPDATE (cURL)
#   DELETE /banco/<id>   -> DELETE (cURL)

@app.route('/banco', method='GET')
def action_banco():
    return ctl.render('banco')


@app.route('/banco', method='POST')
def action_banco_create():
    titulo = request.forms.getunicode('titulo')
    diretor = request.forms.getunicode('diretor')
    ano = request.forms.get('ano')
    return ctl.create_filme(titulo, diretor, ano)


@app.route('/banco/<id:int>', method='PUT')
def action_banco_update(id):
    titulo = request.forms.getunicode('titulo')
    diretor = request.forms.getunicode('diretor')
    ano = request.forms.get('ano')
    return ctl.update_filme(id, titulo, diretor, ano)


@app.route('/banco/<id:int>', method='DELETE')
def action_banco_delete(id):
    return ctl.delete_filme(id)


#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)
