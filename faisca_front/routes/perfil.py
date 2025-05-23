from flask import render_template, request, redirect, url_for, session, Blueprint, flash
import requests
from config import API_BASE_URL
import os

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/')
def perfil():
    headers = {"Authorization": f"Bearer {session.get('access_token', '')}"}
    
    # Inicializar variáveis padrão
    user_data = {}
    livros_data = []
    postagens_data = []
    error_message = None
    
    try:
        # Buscar dados do usuário
        user_response = requests.get(f"{API_BASE_URL}/perfil", headers=headers, timeout=10)
        if user_response.status_code == 200:
            user_data = user_response.json()
        else:
            print(f"Erro ao buscar dados do usuário: {user_response.status_code}")

        # Buscar livros do usuário
        try:
            livros_response = requests.get(f"{API_BASE_URL}/livros/minhasobras", headers=headers, timeout=10)
            if livros_response.status_code == 200:
                livros_data = livros_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar livros: {str(e)}")

        # Buscar postagens do usuário
        try:
            postagens_response = requests.get(f"{API_BASE_URL}/postagens/minhasatualizacoes", headers=headers, timeout=10)
            if postagens_response.status_code == 200:
                postagens_data = postagens_response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar postagens: {str(e)}")

    except requests.exceptions.RequestException as e:
        print(f"Erro crítico ao conectar com a API: {str(e)}")
        error_message = "Erro ao conectar com o servidor. Alguns dados podem não estar disponíveis."
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        error_message = "Ocorreu um erro inesperado ao carregar o perfil."

    # Preparar dados para o template
    template_data = {
        'username': user_data.get('username', session.get('username', '')),
        'nome': user_data.get('nome', ''),
        'bio': user_data.get('bio', ''),
        'profile_pic': user_data.get('profilepic', ''),
        'livros': livros_data if isinstance(livros_data, list) else [],
        'postagens': postagens_data if isinstance(postagens_data, list) else [],
        'error': error_message
    }
    
    return render_template('perfil.html', **template_data)

@perfil_bp.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('perfil.perfil'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('perfil.perfil'))

    # Validar tipo de arquivo
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    
    if file_extension not in allowed_extensions:
        flash('Tipo de arquivo não permitido. Use PNG, JPG, JPEG, GIF ou WEBP.', 'error')
        return redirect(url_for('perfil.perfil'))

    try:
        # Enviar para API
        files = {'file': (file.filename, file.stream, file.mimetype)}
        response = requests.post(
            f"{API_BASE_URL}/perfil/upload_profile_pic",
            files=files,
            headers={"Authorization": f"Bearer {session.get('access_token', '')}"},
            timeout=30
        )
        
        if response.status_code == 200:
            flash('Foto de perfil atualizada com sucesso!', 'success')
            # Atualiza a imagem na sessão
            response_data = response.json()
            if 'filepath' in response_data:
                session['profile_pic'] = response_data['filepath']
        else:
            error_msg = 'Erro ao atualizar foto de perfil'
            try:
                error_detail = response.json().get('detail', error_msg)
                flash(error_detail, 'error')
            except:
                flash(error_msg, 'error')
                
    except requests.exceptions.Timeout:
        flash('Timeout ao enviar arquivo. Tente novamente.', 'error')
    except requests.exceptions.RequestException as e:
        flash(f'Erro de conexão: {str(e)}', 'error')
    except Exception as e:
        flash(f'Erro inesperado: {str(e)}', 'error')
    
    return redirect(url_for('perfil.perfil'))