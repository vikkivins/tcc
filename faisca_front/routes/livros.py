from flask import render_template, request, redirect, url_for, session, Blueprint
from datetime import datetime
import requests, jwt
#from . import livros_bp
from config import API_BASE_URL

livros_bp = Blueprint('livros', __name__)


@livros_bp.route('/create-livro', methods=['GET', 'POST'])
def create_livro():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        capa = request.files['capa'] if 'capa' in request.files else None
        
        livro_data = {
            'titulolivro': titulo,
            'descricaolivro': descricao,
            'datacriacao': datetime.now().strftime('%Y-%m-%d')
        }
        
        try:
            headers = {'Authorization': f"Bearer {session['access_token']}"}
            
            # Se há uma capa, faça upload separado
            if capa:
                files = {'capalivro': (capa.filename, capa.stream, capa.mimetype)}
                response = requests.post(
                    f"{API_BASE_URL}/livros/",
                    data=livro_data,
                    files=files,
                    headers=headers
                )
            else:
                response = requests.post(
                    f"{API_BASE_URL}/livros/",
                    json=livro_data,
                    headers=headers
                )
            
            if response.status_code == 200:
                return redirect(url_for('home.home'))
            
            error_msg = "Erro ao criar livro"
            return render_template('create_livro.html', error=error_msg)
        
        except requests.exceptions.RequestException:
            error_msg = "Erro ao conectar com o servidor"
            return render_template('create_livro.html', error=error_msg)
    
    return render_template('create_livro.html')

@livros_bp.route('/livro/<int:livro_id>')
def visualizar_livro(livro_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    response = requests.get(f"{API_BASE_URL}/livros/{livro_id}", headers=headers)

    if response.status_code == 200:
        livro_data = response.json()    
        return render_template(
            'livro.html',
            livro=livro_data['livro'], 
            capitulos=livro_data.get('capitulos', []),
            ideias=livro_data.get('ideias', [])
            )
    
    return render_template('livro.html', error=f"Erro {response.status_code}: {response.text}")


@livros_bp.route('/edit-livro/<int:livro_id>', methods=['GET', 'POST'])
def edit_livro(livro_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        user_id = session.get('user_id')
        
        # Obter dados do livro
        response = requests.get(
            f"{API_BASE_URL}/livros/{livro_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            return redirect(url_for('home.home'))
        
        livro = response.json()
        
        # Debug para verificar os dados retornados
        # print("Resposta da API:", livro)
        
        livro = livro.get('livro', {})  # Pegamos apenas os dados do livro 

        if request.method == 'POST':
            titulo = request.form['titulolivro']
            descricao = request.form['descricaolivro']
            capa = request.files['capalivro'] if 'capa' in request.files else None  # Capa inicializada corretamente
            
            livro_data = {
                'titulolivro': titulo,
                'descricaolivro': descricao,
                'data_criacao': livro.get('datacriacao', None),  # Retorna None se a chave não existir
                'autor_ultima_modificacao': user_id
            }

            # Se a capa existir no dicionário do livro, mantém
            if not capa and 'capalivro' in livro:
                livro_data['capalivro'] = livro['capalivro']

            # Enviar atualização para API
            update_response = requests.put(
                f"{API_BASE_URL}/livros/{livro_id}",
                headers=headers,
                json=livro_data
            )

            if update_response.status_code == 200:
                return redirect(url_for('home.home'))  # Redireciona após sucesso

        return render_template('edit_livro.html', livro=livro)
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Erro ao conectar com o servidor: {str(e)}"
        return render_template('edit_livro.html', livro=livro, error=error_msg)


@livros_bp.route('/delete-livro/<int:livro_id>', methods=['POST'])
def delete_livro(livro_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        response = requests.delete(
            f"{API_BASE_URL}/livros/{livro_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return redirect(url_for('home.home'))
        
        return redirect(url_for('home.home'))
    
    except requests.exceptions.RequestException:
        return redirect(url_for('home.home'))