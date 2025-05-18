from flask import render_template, request, redirect, url_for, session, Blueprint, flash
import requests
from config import API_BASE_URL
import os

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/')
def perfil():
    # Buscar dados do usuário da API
    user_data = requests.get(f"{API_BASE_URL}/perfil", headers={"Authorization": f"Bearer {session['access_token']}"}).json()
    return render_template('perfil.html', 
                         username=session.get('username', ''),
                         profile_pic=user_data.get('profilepic'))

@perfil_bp.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('perfil.perfil'))
    
    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('perfil.perfil'))

    try:
        # Enviar para API
        files = {'file': (file.filename, file.stream, file.mimetype)}
        response = requests.post(
            f"{API_BASE_URL}/perfil/upload_profile_pic",
            files=files,
            headers={"Authorization": f"Bearer {session['access_token']}"}
        )
        
        if response.status_code == 200:
            flash('Foto de perfil atualizada com sucesso!', 'success')
            # Atualiza a imagem na sessão
            session['profile_pic'] = response.json().get('filepath')
        else:
            flash(response.json().get('detail', 'Erro ao atualizar foto de perfil'), 'error')
    except Exception as e:
        flash(f'Erro ao conectar com o servidor: {str(e)}', 'error')
    
    return redirect(url_for('perfil.perfil'))