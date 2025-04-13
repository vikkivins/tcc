from flask import render_template, request, redirect, url_for, session, Blueprint
from datetime import datetime
import requests, json
#from . import capitulos_bp
from config import API_BASE_URL

capitulos_bp = Blueprint('capitulos', __name__)

@capitulos_bp.route('/create-capitulo/<int:livro_id>', methods=['GET', 'POST'])
def create_capitulo(livro_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        
        capitulo_data = {
            'titulocapitulo': titulo,
            'conteudocapitulo': conteudo,
            'livro_id': livro_id,
            'data_criacao': datetime.now().isoformat()
        }

        print(json.dumps(capitulo_data, indent=4))  # Verifique a saída antes de enviar
        
        try:
            headers = {'Authorization': f"Bearer {session['access_token']}"}
            response = requests.post(f"{API_BASE_URL}/capitulos/", json=capitulo_data, headers=headers)
            print(response.status_code)
            print(response.text)
            
            if response.status_code == 200:
                return redirect(url_for('livros.visualizar_livro', livro_id=livro_id))
            
            error_msg = "Erro ao criar capítulo"
            return render_template('create_capitulo.html', error=error_msg)
        
        except requests.exceptions.RequestException:
            error_msg = "Erro ao conectar com o servidor"
            return render_template('create_capitulo.html', error=error_msg)
    
    return render_template('create_capitulo.html')

@capitulos_bp.route('/capitulo/<int:capitulo_id>')
def visualizar_capitulo(capitulo_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.get(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
    
    if response.status_code == 200:
        capitulo_data = response.json()
        print("Status Code:", response.status_code)
        print("Response JSON:", response.json())
        return render_template('capitulo.html', capitulo=capitulo_data)  # ✅ Usa o JSON direto
    
    return render_template('capitulo.html', error=f"Erro {response.status_code}: {response.text}")

@capitulos_bp.route('/edit-capitulo/<int:capitulo_id>', methods=['GET', 'POST'])
def edit_capitulo(capitulo_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
        
        if response.status_code != 200:
            return redirect(url_for('home.home'))
        
        capitulo = response.json()
        
        if request.method == 'POST':
            titulocapitulo = request.form['titulocapitulo']
            conteudocapitulo = request.form['conteudocapitulo']
            
            capitulo_data = {
                'titulocapitulo': titulocapitulo,
                'conteudocapitulo': conteudocapitulo,
                'data_criacao': capitulo['data_criacao']
            }
            
            try:

                update_response = requests.put(f"{API_BASE_URL}/capitulos/{capitulo_id}", json=capitulo_data, headers=headers)
                
                if update_response.status_code == 200:
                    return redirect(url_for('livros.visualizar_livro', livro_id=capitulo['livro_id']))
                
                error_msg = "Erro ao atualizar capítulo: " + update_response.text
                return render_template('edit_capitulo.html', capitulo=capitulo, error=error_msg)
            
            except requests.exceptions.RequestException as e:
                error_msg = f"Erro na requisição: {str(e)}"
                return render_template('edit_capitulo.html', capitulo=capitulo, error=error_msg)
        
        return render_template('edit_capitulo.html', capitulo=capitulo)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao conectar com o servidor: {str(e)}"
        return render_template('edit_capitulo.html', capitulo=capitulo, error=error_msg)

@capitulos_bp.route('/delete-capitulo/<int:capitulo_id>', methods=['POST'])
def delete_capitulo(capitulo_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.delete(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
        
        if response.status_code == 200:
            return redirect(url_for('home.home'))
        
        return redirect(url_for('home.home'))
    
    except requests.exceptions.RequestException:
        return redirect(url_for('home.home'))