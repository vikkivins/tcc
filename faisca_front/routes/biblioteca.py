from flask import render_template, request, redirect, url_for, session, Blueprint, jsonify, flash
import requests
from config import API_BASE_URL

biblioteca_bp = Blueprint('biblioteca', __name__)

@biblioteca_bp.route('/biblioteca')
def biblioteca():
    """Página principal da biblioteca"""
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        # Obter livros da biblioteca
        response = requests.get(
            f"{API_BASE_URL}/biblioteca/",
            headers=headers
        )
        
        if response.status_code == 200:
            biblioteca_livros = response.json()
            return render_template(
                'biblioteca.html',
                username=session.get('username', ''),
                biblioteca_livros=biblioteca_livros
            )
        
        return render_template('biblioteca.html', 
                             username=session.get('username', ''),
                             biblioteca_livros=[],
                             error=f"Erro {response.status_code}: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
        return render_template('biblioteca.html', 
                             username=session.get('username', ''),
                             biblioteca_livros=[],
                             error="Erro ao conectar com o servidor")

@biblioteca_bp.route('/biblioteca/adicionar/<int:livro_id>', methods=['POST'])
def adicionar_livro(livro_id):
    """Adiciona um livro à biblioteca"""
    if 'access_token' not in session:
        flash('Você precisa estar logado para adicionar livros à biblioteca.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        response = requests.post(
            f"{API_BASE_URL}/biblioteca/{livro_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            flash('Livro adicionado à biblioteca com sucesso!', 'success')
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('detail', 'Erro desconhecido')
            flash(f'Erro ao adicionar livro: {error_msg}', 'error')
    
    except requests.exceptions.RequestException as e:
        flash('Erro ao conectar com o servidor', 'error')
    
    # Redirecionar para a página de origem ou biblioteca
    return redirect(request.referrer or url_for('biblioteca.biblioteca'))

@biblioteca_bp.route('/biblioteca/remover/<int:livro_id>', methods=['POST'])
def remover_livro(livro_id):
    """Remove um livro da biblioteca"""
    if 'access_token' not in session:
        flash('Você precisa estar logado para remover livros da biblioteca.', 'error')
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        response = requests.delete(
            f"{API_BASE_URL}/biblioteca/{livro_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            flash('Livro removido da biblioteca com sucesso!', 'success')
        else:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get('detail', 'Erro desconhecido')
            flash(f'Erro ao remover livro: {error_msg}', 'error')
    
    except requests.exceptions.RequestException as e:
        flash('Erro ao conectar com o servidor', 'error')
    
    # Redirecionar de volta para a biblioteca
    return redirect(url_for('biblioteca.biblioteca'))

@biblioteca_bp.route('/biblioteca/verificar/<int:livro_id>')
def verificar_livro(livro_id):
    """Verifica se um livro está na biblioteca"""
    if 'access_token' not in session:
        return jsonify({'error': 'Não autenticado'}), 401
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        response = requests.get(
            f"{API_BASE_URL}/biblioteca/verificar/{livro_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'na_biblioteca': False}), response.status_code
    
    except requests.exceptions.RequestException as e:
        return jsonify({'na_biblioteca': False, 'error': 'Erro ao conectar'}), 500