from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from model import Usuario
from CRUD.bibliotecacrud import (adicionar_livro_biblioteca, remover_livro_biblioteca, get_biblioteca_usuario,
                                 verificar_livro_na_biblioteca)
from schemas.bibliotecaschemas import BibliotecaLivroResponse
from schemas.usuarioschemas import AutorResumoResponse
from typing import List

router = APIRouter(tags=['Biblioteca'])

@router.post("/{livro_id}")
def adicionar_livro_na_biblioteca(
    livro_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adiciona um livro à biblioteca do usuário"""
    sucesso = adicionar_livro_biblioteca(db, current_user.id, livro_id)
    
    if not sucesso:
        raise HTTPException(
            status_code=400, 
            detail="Livro já está na sua biblioteca"
        )
    
    return {"message": "Livro adicionado à biblioteca com sucesso"}

@router.delete("/{livro_id}")
def remover_livro_da_biblioteca(
    livro_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove um livro da biblioteca do usuário"""
    sucesso = remover_livro_biblioteca(db, current_user.id, livro_id)
    
    if not sucesso:
        raise HTTPException(
            status_code=404,
            detail="Livro não encontrado na sua biblioteca"
        )
    
    return {"message": "Livro removido da biblioteca com sucesso"}

@router.get("/", response_model=List[BibliotecaLivroResponse])
def get_minha_biblioteca(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna todos os livros da biblioteca do usuário"""
    biblioteca = get_biblioteca_usuario(db, current_user.id)
    
    response = []
    for livro, autor, data_adicao in biblioteca:
        response.append(BibliotecaLivroResponse(
            id=livro.id,
            titulolivro=livro.titulolivro,
            descricaolivro=livro.descricaolivro,
            datacriacao=livro.datacriacao,
            data_adicao=data_adicao,
            autor=AutorResumoResponse(
                username=autor.username,
                profilepic=autor.profilepic
            )
        ))
    
    return response

@router.get("/verificar/{livro_id}")
def verificar_livro_biblioteca(
    livro_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Verifica se um livro está na biblioteca do usuário"""
    na_biblioteca = verificar_livro_na_biblioteca(db, current_user.id, livro_id)
    return {"na_biblioteca": na_biblioteca}