from flask import Blueprint, render_template, session, redirect, url_for
import requests
from config import API_BASE_URL

explorar_bp = Blueprint('explorar', __name__)

@explorar_bp.route('/explorar')
def explorar():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{API_BASE_URL}/explorar/explorar", headers=headers)
        
        if response.status_code == 200:
            explorar_data = response.json()
            return render_template('explorar.html', livros=explorar_data)
        
        return render_template(
            'explorar.html',
            livros=[],
            error=f"Erro {response.status_code}: {response.text}"
        )
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
        return render_template('explorar.html', livros=[], error="Erro ao conectar com o servidor")
