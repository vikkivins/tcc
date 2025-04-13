from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from model import Usuario, Livro, Ideia
from schemas.usuarioschemas import UsuarioResponse
from schemas.livroschemas import LivroResponse
from typing import List

router = APIRouter(prefix='/home', tags=['Home'])

@router.get("/", response_model=dict)
async def get_home_data(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retorna os dados para a página home:
    - Informações do usuário
    - Lista de livros
    - Lista de ideias
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Não autenticado")

    livros = db.query(Livro).filter(Livro.usuario_id == current_user.id).all()

    livros_response = [
        {
            "id": livro.id,
            "titulolivro": livro.titulolivro,
            "descricaolivro": livro.descricaolivro,
            "datacriacao": livro.datacriacao.strftime('%Y-%m-%d') if livro.datacriacao else None
            #,"capalivro": livro.capalivro
        }
        for livro in livros
    ]

    ideias = db.query(Ideia).filter(Ideia.usuario_id == current_user.id).all()

    ideias_response = [
        {
            "id": ideia.id,
            "tituloideia": ideia.tituloideia,
            "conteudoideia": ideia.conteudoideia,
            "datacriacao": ideia.datacriacao.strftime('%Y-%m-%d') if ideia.datacriacao else None
            #, "capaideia": ideia.capaideia
        }
        for ideia in ideias
    ]

    return {
        "usuario": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
        },
        "livros": livros_response,
        "ideias": ideias_response
    }