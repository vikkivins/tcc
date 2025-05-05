# routes/postagem.py

from flask import Blueprint, render_template, session, redirect, url_for, request
import requests
from config import API_BASE_URL

postagem_bp = Blueprint('postagem', __name__)

@postagem_bp.route('/postagens')
def listar_postagens():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))

    # Paginação simples
    page = int(request.args.get('page', 1))
    limit = 5
    skip = (page - 1) * limit

    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        params = {'skip': skip, 'limit': limit}
        response = requests.get(f"{API_BASE_URL}/postagens/", headers=headers, params=params)

        if response.status_code == 200:
            postagens_data = response.json()
            for postagem in postagens_data:
                if 'usuario' not in postagem and 'usuario_id' in postagem:
                    try:
                        user_response = requests.get(f"{API_BASE_URL}/usuarios/{postagem['usuario_id']}", headers=headers)
                        if user_response.status_code == 200:
                            postagem['usuario'] = user_response.json()
                        else:
                            postagem['usuario'] = {'username': f"Usuário #{postagem['usuario_id']}"}
                    except:
                        postagem['usuario'] = {'username': f"Usuário #{postagem['usuario_id']}"}

            print("Dados recebidos da API:", postagens_data)
            return render_template('postagem.html', postagens=postagens_data, page=page)

        return render_template(
            'postagem.html',
            postagens=[],
            error=f"Erro {response.status_code}: {response.text}",
            page=page
        )

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
        return render_template('postagem.html', postagens=[], error="Erro ao conectar com o servidor", page=page)
    
@postagem_bp.route('/postagens/nova', methods=['POST'])
def nova_postagem():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))

    conteudo = request.form.get('conteudopostagem')
    datacriacao = request.form.get('datacriacao')

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    payload = {
        "conteudopostagem": conteudo,
        "datacriacao": datacriacao,
        "postagem_id": None
    }

    response = requests.post(f"{API_BASE_URL}/postagens/", headers=headers, json=payload)

    return redirect(url_for('postagem.listar_postagens'))

@postagem_bp.route('/postagens/editar/<int:id>', methods=['POST'])
def editar_postagem(id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))

    conteudo = request.form.get('conteudopostagem')
    datacriacao = request.form.get('datacriacao')
    
    print(f"Editando postagem {id} com conteúdo: {conteudo} e data: {datacriacao}")

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    payload = {
        "conteudopostagem": conteudo,
        "datacriacao": datacriacao
    }

    try:
        response = requests.put(f"{API_BASE_URL}/postagens/{id}", headers=headers, json=payload)
        
        if response.status_code == 200:
            print("Postagem atualizada com sucesso")
        else:
            print(f"Erro ao atualizar postagem: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Erro ao enviar requisição: {str(e)}")

    return redirect(url_for('postagem.listar_postagens'))

@postagem_bp.route('/postagens/excluir/<int:id>', methods=['POST'])
def excluir_postagem(id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))

    headers = {'Authorization': f"Bearer {session['access_token']}"}
    
    try:
        response = requests.delete(f"{API_BASE_URL}/postagens/{id}", headers=headers)
        
        if response.status_code == 200:
            print("Postagem excluída com sucesso")
        else:
            print(f"Erro ao excluir postagem: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Erro ao enviar requisição: {str(e)}")

    return redirect(url_for('postagem.listar_postagens'))

