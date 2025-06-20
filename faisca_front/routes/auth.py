from flask import Blueprint, render_template, request, redirect, url_for, session
import requests, jwt
#from . import auth_bp
from config import API_BASE_URL

auth_bp = Blueprint('auth', __name__)

#TODO: Adicionar a parte de senhas seguras. Letras maiúsculas e minúsculas, qtd de caracteres, um especial etc

@auth_bp.route('/')
def index():
    if 'access_token' in session:
        return redirect(url_for('biblioteca.biblioteca'))
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me')
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/login/token",
                data={
                    'username': username,
                    'password': password
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                session['access_token'] = token_data['access_token']
                
                # Obter informações do usuário
                decoded = jwt.decode(token_data['access_token'], options={"verify_signature": False})
                session['user_id'] = decoded.get('user_id')
                session['username'] = decoded.get('sub')
                
                return redirect(url_for('biblioteca.biblioteca'))
            
            error_msg = "Usuário ou senha incorretos"
            return render_template('login.html', error=error_msg)
            
        except requests.exceptions.RequestException:
            error_msg = "Erro ao conectar com o servidor"
            return render_template('login.html', error=error_msg)
    
    # Verificar se há mensagem de sucesso do registro
    success_msg = request.args.get('success')
    return render_template('login.html', success=success_msg)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

####################################################
################# AUTENTICAÇÃO, CADASTRO #########################
####################################################

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Coletar dados do formulário (senha em texto puro)
            form_data = {
                'nome': request.form['nome'],
                'username': request.form['username'],
                'dtnasc': request.form['dtnasc'],
                'email': request.form['email'],
                'senha': request.form['senha'],  # Senha em texto puro
                'bio': request.form.get('bio', ''),
                'pronome': request.form.get('pronome', '')
            }

            # Enviar para a API (a senha será hasheada no backend)
            response = requests.post(
                f"{API_BASE_URL}/usuarios/",
                json=form_data
            )

            if response.status_code == 200:
                # Em vez de fazer login automático, redirecionar para a página de login
                success_msg = "Cadastro realizado com sucesso! Faça login para continuar."
                return redirect(url_for('auth.login', success=success_msg))
            
            # Tratar erros específicos da API
            error_detail = response.json().get('detail', 'Erro desconhecido')
            return render_template('register.html', 
                               error=f"Erro no cadastro: {error_detail}",
                               form_data=request.form)
            
        except Exception as e:
            return render_template('register.html', 
                               error=f"Erro no sistema: {str(e)}",
                               form_data=request.form)
    
    return render_template('register.html')

def get_current_user():
    if 'access_token' not in session:
        return None
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(
            f"{API_BASE_URL}/usuarios/me",
            headers=headers
        )
        
        if response.status_code == 200:
            return response.json()
        
        return None
    except requests.exceptions.RequestException:
        return None