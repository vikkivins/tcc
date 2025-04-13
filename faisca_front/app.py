from flask import Flask
from routes.auth import auth_bp
from routes.usuario import usuario_bp
from routes.capitulos import capitulos_bp
from routes.home import home_bp
from routes.ideias import ideias_bp
from routes.livros import livros_bp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Mude para uma chave segura em produção

app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(livros_bp, url_prefix='/livros')
app.register_blueprint(capitulos_bp, url_prefix='/capitulos')
app.register_blueprint(ideias_bp, url_prefix='/ideias')
app.register_blueprint(usuario_bp, url_prefix='/usuario')

if __name__ == '__main__':
    app.run(debug=True, port=5000)