<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banco de Filmes</title>
    <link rel="stylesheet" type="text/css" href="/static/css/filmes.css">
</head>
<body>
    <div class="caixa">
        <h1>Banco - Filmes cadastrados</h1>
        <p>Usuário autenticado: <b>{{current_user.username}}</b></p>

        % if filmes:
        <table>
            <tr><th>ID</th><th>Título</th><th>Diretor</th><th>Ano</th></tr>
            % for filme in filmes:
            <tr>
                <td>{{filme.id}}</td>
                <td>{{filme.titulo}}</td>
                <td>{{filme.diretor}}</td>
                <td>{{filme.ano}}</td>
            </tr>
            % end
        </table>
        % else:
        <p>Nenhum filme cadastrado.</p>
        % end

        <form action="/logout" method="post">
            <button type="submit">Logout</button>
        </form>
    </div>
</body>
</html>
