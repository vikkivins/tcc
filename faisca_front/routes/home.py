from flask import render_template, request, redirect, url_for, session, Blueprint
import requests, jwt
#from . import home_bp
from config import API_BASE_URL

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        # Obter dados do endpoint home
        response = requests.get(
            f"{API_BASE_URL}/home/",
            headers=headers
        )
        
        if response.status_code == 200:
            home_data = response.json()
            return render_template(
                'home.html',
                username=home_data['usuario']['username'],
                livros=home_data['livros'],
                ideias=home_data['ideias']
            )
        
        return render_template('home.html', 
                             username=session.get('username', ''),
                             livros=[], 
                             ideias=[],
                             error=f"Erro {response.status_code}: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
        return render_template('home.html', 
                           username=session.get('username', ''),
                           livros=[], 
                           error="Erro ao conectar com o servidor")