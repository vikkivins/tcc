from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from model import Usuario, Livro, Ideia
from schemas.usuarioschemas import UsuarioResponse
from schemas.livroschemas import LivroResponse
from typing import List

router = APIRouter(prefix='/perfil', tags=['Perfil'])

#@router.get("/", response_model=dict)