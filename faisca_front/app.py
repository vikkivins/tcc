from flask import Flask, session
from routes.auth import auth_bp
from routes.usuario import usuario_bp
from routes.capitulos import capitulos_bp
from routes.biblioteca import biblioteca_bp
from routes.ideias import ideias_bp
from routes.livros import livros_bp
from routes.explorar import explorar_bp
from routes.postagens import postagem_bp
from routes.perfil import perfil_bp
from routes.followers import followers_bp
from routes.notificacoes import notificacoes_bp, get_notificacoes_header

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Mude para uma chave segura em produção

app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(biblioteca_bp, url_prefix='/biblioteca')
app.register_blueprint(explorar_bp, url_prefix='/explorar')
app.register_blueprint(livros_bp, url_prefix='/livros')
app.register_blueprint(capitulos_bp, url_prefix='/capitulos')
app.register_blueprint(ideias_bp, url_prefix='/ideias')
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(postagem_bp, url_prefix='/postagens')
app.register_blueprint(perfil_bp, url_prefix='/perfil')
app.register_blueprint(followers_bp, url_prefix='/followers')
app.register_blueprint(notificacoes_bp, url_prefix='/notificacoes')


@app.context_processor
def inject_notificacoes():
    user_id = session.get('user_id')
    notificacoes_header = get_notificacoes_header(user_id) if user_id else []
    return dict(notificacoes_header=notificacoes_header)


if __name__ == '__main__':
    app.run(debug=True, port=5000)