from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
import requests

notificacoes_bp = Blueprint('notificacoes', __name__)

@notificacoes_bp.route('/notificacoes')
def notificacoes():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    # Buscar todas as notificações do usuário
    # Supondo que o endpoint FastAPI seja /notificacoes/{usuario_id}
    api_url = f"http://localhost:8000/notificacoes/{user_id}"
    response = requests.get(api_url)
    notificacoes = response.json() if response.status_code == 200 else []
    return render_template('notificacoes.html', notificacoes=notificacoes)

@notificacoes_bp.route('/api/notificacoes/nao_visualizadas')
def notificacoes_nao_visualizadas():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])
    api_url = f"http://localhost:8000/notificacoes/{user_id}?apenas_nao_lidas=true&limit=5"
    response = requests.get(api_url)
    notificacoes = response.json() if response.status_code == 200 else []
    return jsonify(notificacoes)

@notificacoes_bp.route('/api/notificacoes/marcar_como_lidas', methods=['POST'])
def marcar_notificacoes_como_lidas():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False}), 401
    api_url = f"http://localhost:8000/notificacoes/{user_id}/marcar_como_lidas"
    response = requests.post(api_url)
    return jsonify({'success': response.status_code == 200})

@notificacoes_bp.route('/api/notificacoes/recentes')
def notificacoes_recentes():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify([])
    api_url = f"http://localhost:8000/notificacoes/{user_id}?limit=5"
    response = requests.get(api_url)
    notificacoes = response.json() if response.status_code == 200 else []
    return jsonify(notificacoes)

def get_notificacoes_header(user_id):
    api_url = f"http://localhost:8000/notificacoes/{user_id}?limit=5"
    response = requests.get(api_url)
    return response.json() if response.status_code == 200 else []
