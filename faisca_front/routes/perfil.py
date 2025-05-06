from flask import render_template, request, redirect, url_for, session, Blueprint, Response
import requests, jwt
from config import API_BASE_URL

perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/perfil')
def perfil():
    return render_template('perfil.html', 
                             username=session.get('username', ''))