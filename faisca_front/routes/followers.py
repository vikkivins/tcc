from flask import Blueprint, render_template, request
import requests
from flask import session, redirect, url_for

followers_bp = Blueprint('followers', __name__)

@followers_bp.route('/<int:usuario_id>/seguidores')
def seguidores(usuario_id):
    # Chama a API do backend para pegar os seguidores
    response = requests.get(f'http://localhost:8000/followers/{usuario_id}/seguidores')
    usuarios = response.json() if response.status_code == 200 else []
    return render_template('seguidores.html', usuarios=usuarios, titulo_pagina='Seguidores')

@followers_bp.route('/<int:usuario_id>/seguindo')
def seguindo(usuario_id):
    # Chama a API do backend para pegar quem o usuário está seguindo
    response = requests.get(f'http://localhost:8000/followers/{usuario_id}/seguindo')
    usuarios = response.json() if response.status_code == 200 else []
    return render_template('seguindo.html', usuarios=usuarios, titulo_pagina='Seguindo')
