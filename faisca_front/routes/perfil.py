from flask import render_template, request, redirect, url_for, session, Blueprint, flash
import requests
from config import API_BASE_URL
import os

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/')
@perfil_bp.route('/<username>')
def perfil(username=None):
    headers = {"Authorization": f"Bearer {session.get('access_token', '')}"}
    
    # Se não há username na URL, usar o próprio usuário logado
    if not username:
        username = session.get('username')
        if not username:
            flash('Você precisa estar logado para acessar o perfil', 'error')
            return redirect(url_for('auth.login'))
    
    # Inicializar variáveis padrão
    user_data = {}
    livros_data = []
    postagens_data = []
    error_message = None
    
    try:
        # Buscar dados do perfil (funciona tanto para próprio perfil quanto para outros usuários)
        user_response = requests.get(f"{API_BASE_URL}/perfil/{username}", headers=headers, timeout=10)
        
        if user_response.status_code == 404:
            flash('Usuário não encontrado', 'error')
            return redirect(url_for('perfil.perfil'))
        elif user_response.status_code == 401:
            flash('Sessão expirada. Faça login novamente.', 'error')
            return redirect(url_for('auth.login'))
        elif user_response.status_code == 200:
            profile_data = user_response.json()
            user_data = {
                'username': profile_data.get('username', ''),
                'nome': profile_data.get('nome', ''),
                'bio': profile_data.get('bio', ''),
                'pronome': profile_data.get('pronome', ''),
                'profilepic': profile_data.get('profilepic')
            }
            livros_data = profile_data.get('livros', [])
            is_own_profile = profile_data.get('is_own_profile', False)
            
            try:
                if is_own_profile:
                    # Para o próprio perfil, buscar todas as postagens
                    postagens_response = requests.get(f"{API_BASE_URL}/postagens/minhasatualizacoes", headers=headers, timeout=10)
                else:
                    # Para outros usuários, buscar postagens públicas
                    postagens_response = requests.get(f"{API_BASE_URL}/postagens/{username}", headers=headers, timeout=10)
                
                if postagens_response.status_code == 200:
                    postagens_data = postagens_response.json()
            except requests.exceptions.RequestException as e:
                print(f"Erro ao buscar postagens: {str(e)}")
                # Não é erro crítico, continua sem as postagens
            
        else:
            print(f"Erro ao buscar perfil do usuário {username}: {user_response.status_code}")
            error_message = "Erro ao carregar perfil do usuário."

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API: {str(e)}")
        error_message = "Erro ao conectar com o servidor. Alguns dados podem não estar disponíveis."
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        error_message = "Ocorreu um erro inesperado ao carregar o perfil."

    # Preparar dados para o template
    template_data = {
        'username': user_data.get('username', username),
        'nome': user_data.get('nome', ''),
        'bio': user_data.get('bio', ''),
        'pronome': user_data.get('pronome', ''),
        'profile_pic': user_data.get('profilepic', ''),
        'livros': livros_data if isinstance(livros_data, list) else [],
        'postagens': postagens_data if isinstance(postagens_data, list) else [],
        'error': error_message,
        'is_own_profile': locals().get('is_own_profile', False),
        'viewing_username': username
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