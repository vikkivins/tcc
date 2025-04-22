from flask import render_template, request, redirect, url_for, session, Blueprint, jsonify
from datetime import datetime, timezone
import requests, json
#from . import capitulos_bp
from config import API_BASE_URL
import jwt

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
        
        # Pega o id do usuário logado a partir do token
        token = session['access_token']
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        usuario_logado = decoded_token.get("user_id")
        
        # Verifica se o usuário é autor do capítulo
        eh_autor = int(usuario_logado) == int(capitulo_data.get('usuario_id', 0))
        
        # Verificar se há comentários e adicionar informações de usuário se necessário
        if 'comentarios' in capitulo_data:
            for comentario in capitulo_data['comentarios']:
                # Verifica se o usuário é autor do comentário
                comentario['eh_autor'] = int(usuario_logado) == int(comentario.get('usuario_id', 0))
                
                if 'usuario' not in comentario and 'usuario_id' in comentario:
                    # Buscar informações do usuário se necessário
                    try:
                        user_response = requests.get(f"{API_BASE_URL}/usuarios/{comentario['usuario_id']}", headers=headers)
                        if user_response.status_code == 200:
                            comentario['usuario'] = user_response.json()
                        else:
                            comentario['usuario'] = {'username': f"Usuário #{comentario['usuario_id']}"}
                    except:
                        comentario['usuario'] = {'username': f"Usuário #{comentario['usuario_id']}"}
                
                # Processar respostas recursivamente
                if 'respostas' in comentario:
                    for resposta in comentario['respostas']:
                        # Verifica se o usuário é autor da resposta
                        resposta['eh_autor'] = int(usuario_logado) == int(resposta.get('usuario_id', 0))
                        
                        if 'usuario' not in resposta and 'usuario_id' in resposta:
                            # Mesmo processo para cada resposta
                            try:
                                user_response = requests.get(f"{API_BASE_URL}/usuarios/{resposta['usuario_id']}", headers=headers)
                                if user_response.status_code == 200:
                                    resposta['usuario'] = user_response.json()
                                else:
                                    resposta['usuario'] = {'username': f"Usuário #{resposta['usuario_id']}"}
                            except:
                                resposta['usuario'] = {'username': f"Usuário #{resposta['usuario_id']}"}
        
        return render_template('capitulo.html', 
                             capitulo=capitulo_data,
                             eh_autor=eh_autor)
    
    return render_template('capitulo.html', 
                         error=f"Erro {response.status_code}: {response.text}", 
                         capitulo={"id": capitulo_id, "comentarios": []},
                         eh_autor=False)

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
    
########## COMENTARIOS #######################

@capitulos_bp.route('/capitulo/<int:capitulo_id>/comentario', methods=['POST'])
def adicionar_comentario(capitulo_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    # Obter dados do formulário
    conteudo = request.form.get('conteudo')
    comentario_pai_id = request.form.get('comentario_id') or None
    
    if not conteudo:
        # Carregar capítulo para mostrar o erro
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
        
        if response.status_code != 200:
            return redirect(url_for('home.home', error_msg="Erro ao carregar capítulo"))
        
        capitulo = response.json()
        return render_template('capitulo.html', 
                            error_msg="O comentário não pode estar vazio",
                            capitulo=capitulo)
    
    # Preparar dados para a API
    comentario_data = {
        "conteudocomentario": conteudo,
        "capitulo_id": capitulo_id,
        "comentario_id": comentario_pai_id,
        "datacriacao": datetime.now(timezone.utc).isoformat()
    }
    
    try:
        headers = {
            'Authorization': f"Bearer {session['access_token']}",
            'Content-Type': 'application/json'
        }
        
        # Converter para JSON antes de enviar
        response = requests.post(
            f"{API_BASE_URL}/capitulos/{capitulo_id}/comentarios",
            json=comentario_data,  # Usar json= para enviar como JSON
            headers=headers
        )
        
        if response.status_code != 200:
            # Recarregar capítulo para mostrar erro
            response_cap = requests.get(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
            if response_cap.status_code != 200:
                return redirect(url_for('home.home', error_msg="Erro ao carregar capítulo"))
            
            capitulo = response_cap.json()
            return render_template('capitulo.html',
                                error_msg="Erro ao adicionar comentário: " + response.text,
                                capitulo=capitulo, session=session)
        
    except requests.exceptions.RequestException as e:
        # Recarregar capítulo para mostrar erro de conexão
        try:
            response_cap = requests.get(f"{API_BASE_URL}/capitulos/{capitulo_id}", headers=headers)
            if response_cap.status_code != 200:
                return redirect(url_for('home.home', error_msg="Erro ao carregar capítulo"))
            
            capitulo = response_cap.json()
            return render_template('capitulo.html',
                                error_msg=f"Erro ao conectar com o servidor: {str(e)}",
                                capitulo=capitulo)
        except requests.exceptions.RequestException:
            return redirect(url_for('home.home', error_msg="Erro grave ao conectar com o servidor"))

    return redirect(url_for('capitulos.visualizar_capitulo', capitulo_id=capitulo_id))


@capitulos_bp.route('/comentario/<int:comentario_id>/editar', methods=['GET', 'POST'])
def editar_comentario(comentario_id):
    if 'access_token' not in session:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Não autenticado'}), 401
        return redirect(url_for('auth.login'))
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    capitulo_id = request.args.get('capitulo_id')
    
    if request.method == 'POST':
        conteudo = request.form.get('conteudo')
        
        if not conteudo:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'error': 'O comentário não pode estar vazio'}), 400
            return render_template('editar_comentario.html',
                                error_msg="O comentário não pode estar vazio",
                                comentario_id=comentario_id,
                                capitulo_id=capitulo_id)
        
        try:
            response = requests.put(
                f"{API_BASE_URL}/comentarios/{comentario_id}",
                json={'conteudocomentario': conteudo},
                headers=headers
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if response.status_code == 200:
                    return jsonify({
                        'success': True,
                        'conteudo': conteudo
                    })
                return jsonify({
                    'success': False,
                    'error': response.text
                }), response.status_code
            
            if response.status_code != 200:
                return render_template('editar_comentario.html',
                                    error_msg="Erro ao atualizar comentário",
                                    comentario_id=comentario_id,
                                    capitulo_id=capitulo_id)
            
            return redirect(url_for('capitulos.visualizar_capitulo', 
                                capitulo_id=capitulo_id))
        
        except requests.exceptions.RequestException as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'error': f"Erro ao conectar com o servidor: {str(e)}"
                }), 500
            return render_template('editar_comentario.html',
                                error_msg=f"Erro ao conectar com o servidor: {str(e)}",
                                comentario_id=comentario_id,
                                capitulo_id=capitulo_id)
    
    # GET - Mostrar formulário de edição (mantido para compatibilidade)
    try:
        response = requests.get(
            f"{API_BASE_URL}/comentarios/{comentario_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            comentario = response.json()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': True,
                    'comentario': comentario
                })
            return render_template('editar_comentario.html', 
                                comentario=comentario,
                                capitulo_id=capitulo_id)
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'success': False,
                    'error': 'Comentário não encontrado'
                }), 404
            return redirect(url_for('capitulos.visualizar_capitulo',
                                capitulo_id=capitulo_id,
                                error_msg="Comentário não encontrado"))
    
    except requests.exceptions.RequestException as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': False,
                'error': f"Erro ao conectar com o servidor: {str(e)}"
            }), 500
        return redirect(url_for('capitulos.visualizar_capitulo',
                            capitulo_id=capitulo_id,
                            error_msg=f"Erro ao conectar com o servidor: {str(e)}"))

@capitulos_bp.route('/comentario/<int:comentario_id>/excluir', methods=['POST'])
def excluir_comentario(comentario_id):
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    headers = {'Authorization': f"Bearer {session['access_token']}"}
    capitulo_id = request.args.get('capitulo_id')
    
    try:
        response = requests.delete(
            f"{API_BASE_URL}/comentarios/{comentario_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            return redirect(url_for('capitulos.visualizar_capitulo',
                                capitulo_id=capitulo_id,
                                error_msg="Erro ao excluir comentário"))
        
    except requests.exceptions.RequestException as e:
        return redirect(url_for('capitulos.visualizar_capitulo',
                            capitulo_id=capitulo_id,
                            error_msg=f"Erro ao conectar com o servidor: {str(e)}"))
    
    return redirect(url_for('capitulos.visualizar_capitulo', 
                        capitulo_id=capitulo_id))