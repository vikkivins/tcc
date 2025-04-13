from flask import render_template, request, redirect, url_for, session, Blueprint
#from . import usuario_bp
import requests
from config import API_BASE_URL

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/configuracoes', methods=['GET', 'POST'])
def user_configuracoes():
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        # Obter dados do usuário
        user_id = session.get('user_id')
        response = requests.get(
            f"{API_BASE_URL}/usuarios/{user_id}",
            headers=headers
        )
        
        if response.status_code != 200:
            return render_template('configuracoes.html', 
                               error="Erro ao carregar dados do usuário",
                               username=session.get('username', ''))
        
        user_data = response.json()
        
        # Processar formulário de atualização
        if request.method == 'POST':
            if 'delete_account' in request.form:
                # Excluir conta
                delete_response = requests.delete(
                    f"{API_BASE_URL}/usuarios/{user_id}",
                    headers=headers
                )
                
                if delete_response.status_code == 200:
                    session.clear()
                    return redirect(url_for('auth.login'))
                else:
                    return render_template('configuracoes.html', 
                                       user=user_data,
                                       error="Erro ao excluir conta",
                                       username=session.get('username', ''))
            
            else:
                # Atualizar dados
                update_data = {
                    'nome': request.form.get('nome', user_data.get('nome', '')),
                    'username': request.form.get('username', user_data.get('username', '')),
                    'dtnasc': request.form.get('dtnasc', user_data.get('dtnasc', '')),
                    'email': request.form.get('email', user_data.get('email', '')),
                    'bio': request.form.get('bio', user_data.get('bio', ''))
                }
                
                # Verificar se a senha foi alterada
                new_password = request.form.get('senha')
                if new_password:
                    update_data['senha'] = new_password
                
                update_response = requests.put(
                    f"{API_BASE_URL}/usuarios/{user_id}",
                    json=update_data,
                    headers=headers
                )
                
                if update_response.status_code == 200:
                    # Atualizar sessão se o username mudou
                    if 'username' in update_data:
                        session['username'] = update_data['username']
                    return redirect(url_for('usuario.user_configuracoes'))
                else:
                    error_detail = update_response.json().get('detail', 'Erro desconhecido')
                    return render_template('configuracoes.html', 
                                       user=user_data,
                                       error=f"Erro ao atualizar: {error_detail}",
                                       username=session.get('username', ''))
        
        return render_template('configuracoes.html', 
                           user=user_data,
                           username=session.get('username', ''))
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {str(e)}")
        return render_template('configuracoes.html', 
                           username=session.get('username', ''),
                           error="Erro ao conectar com o servidor")