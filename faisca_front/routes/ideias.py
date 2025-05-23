from flask import render_template, request, redirect, url_for, session, Blueprint
from datetime import datetime
import requests
#from . import ideias_bp
from config import API_BASE_URL

ideias_bp = Blueprint('ideias', __name__)

@ideias_bp.route('/create-ideia', methods=['GET', 'POST'])
def create_ideia():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        
        ideia_data = {
            'tituloideia': titulo,
            'conteudoideia': conteudo,
            'datacriacao': datetime.now().strftime('%Y-%m-%d')
        }
        
        try:
            headers = {'Authorization': f"Bearer {session['access_token']}"}
            response = requests.post(f"{API_BASE_URL}/ideias/", json=ideia_data, headers=headers)
            
            if response.status_code == 200:
                return redirect(url_for('biblioteca.biblioteca'))
            
            error_msg = "Erro ao criar ideia"
            return render_template('create_ideia.html', error=error_msg)
        
        except requests.exceptions.RequestException:
            error_msg = "Erro ao conectar com o servidor"
            return render_template('create_ideia.html', error=error_msg)
    
    return render_template('create_ideia.html')

@ideias_bp.route('/ideia/<int:ideia_id>')
def visualizar_ideia(ideia_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.get(f"{API_BASE_URL}/ideias/{ideia_id}", headers=headers)
    
    if response.status_code == 200:
        ideia_data = response.json()
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        return render_template('ideia.html', ideia=ideia_data)
    
    return render_template('ideia.html', error=f"Erro {response.status_code}: {response.text}")


@ideias_bp.route('/edit-ideia/<int:ideia_id>', methods=['GET', 'POST'])
def edit_ideia(ideia_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        user_id = session.get('user_id')
        
        response = requests.get(f"{API_BASE_URL}/ideias/{ideia_id}", headers=headers)
        
        if response.status_code != 200:
            return redirect(url_for('biblioteca.biblioteca'))
        
        ideia = response.json()
        
        if request.method == 'POST':
            titulo = request.form['titulo']
            conteudo = request.form['conteudo']
            
            ideia_data = {
                'tituloideia': titulo,
                'conteudoideia': conteudo,
                'datacriacao': ideia['datacriacao']
            }
            
            try:
                update_response = requests.put(f"{API_BASE_URL}/ideias/{ideia_id}", json=ideia_data, headers=headers)
                
                if update_response.status_code == 200:
                    return redirect(url_for('biblioteca.biblioteca'))
                
                error_msg = "Erro ao atualizar ideia: " + update_response.text
                return render_template('edit_ideia.html', ideia=ideia, error=error_msg)
            
            except requests.exceptions.RequestException as e:
                error_msg = f"Erro na requisição: {str(e)}"
                return render_template('edit_ideia.html', ideia=ideia, error=error_msg)
        
        return render_template('edit_ideia.html', ideia=ideia)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao conectar com o servidor: {str(e)}"
        return render_template('edit_ideia.html', ideia=ideia, error=error_msg)

@ideias_bp.route('/delete-ideia/<int:ideia_id>', methods=['POST'])
def delete_ideia(ideia_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.delete(f"{API_BASE_URL}/ideias/{ideia_id}", headers=headers)
        
        return redirect(url_for('biblioteca.biblioteca')) if response.status_code == 200 else redirect(url_for('biblioteca'))
    
    except requests.exceptions.RequestException:
        return redirect(url_for('biblioteca.biblioteca'))