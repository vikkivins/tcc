from CRUD.livrocrud import create_livro, get_livros, get_livro, update_livro, delete_livro
from schemas.livroschemas import LivroCreate, LivroUpdate, LivroResponse, LivroDetalhadoResponse
from schemas.capituloschemas import CapituloResponse
from schemas.ideiaschemas import IdeiaResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db

from model import Usuario, Livro, Ideia, Capitulo
from security import get_current_user

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix='/livros', tags=['Livros'])

# Endpoints para livro
@router.post("/", response_model=LivroResponse)
def create_livro_endpoint(livro: LivroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livro_data = livro.model_dump()
    livro_data['usuario_id'] = current_user.id
    return create_livro(db=db, **livro_data)

@router.get("/", response_model=List[LivroResponse])
def read_livros_endpoint(db: Session = Depends(get_db)):
    return get_livros(db=db)

@router.get("/minhasobras", response_model=List[LivroResponse])
def read_minhas_obras(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livros = db.query(Livro).filter(Livro.usuario_id == current_user.id).all()
    return livros

# para que os livros sejam publicos pra quem não é autenticado
# @router.get("/publicos", response_model=List[LivroResponse])
# def read_livros_publicos_endpoint(db: Session = Depends(get_db)):
#     return db.query(Livro).filter(Livro.publico == True).all()

# Novo endpoint para livros públicos de um usuário específico
@router.get("/publicos/{username}", response_model=List[LivroResponse])
def read_livros_publicos_usuario(username: str, db: Session = Depends(get_db)):
    """Retorna apenas os livros públicos de um usuário específico"""
    # Buscar o usuário pelo username
    user = db.query(Usuario).filter(Usuario.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar apenas livros públicos deste usuário
    livros = db.query(Livro).filter(
        Livro.usuario_id == user.id,
        Livro.publico == True
    ).all()
    
    return livros

@router.put("/{livro_id}", response_model=LivroResponse)
def update_livro_endpoint(livro_id: int, livro: LivroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livro_data = livro.model_dump()
    livro_data['autor_ultima_modificacao'] = current_user.id
    db_livro = update_livro(db=db, livro_id=livro_id, **livro_data)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@router.delete("/{livro_id}", response_model=LivroResponse)
def delete_livro_endpoint(livro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_livro = delete_livro(db=db, livro_id=livro_id)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@router.get("/{livro_id}", response_model=LivroDetalhadoResponse)
def read_livro_endpoint(livro_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Retorna os detalhes de um livro, incluindo:
    - Informações do livro
    - Lista de capítulos
    - Lista de ideias relacionadas (se houver)
    """
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()

    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if db_livro.usuario_id != current_user.id and not db_livro.publico:
        raise HTTPException(status_code=403, detail="Acesso negado")

    capitulos = db.query(Capitulo).filter(Capitulo.livro_id == livro_id).all()
    capitulos_response = [CapituloResponse.model_validate(cap.__dict__) for cap in capitulos]


    # ideias = db.query(Ideia).filter(Ideia.livro_id == livro_id).all()
    # ideias_response = [IdeiaResponse.model_validate(ideia) for ideia in ideias]

    return LivroDetalhadoResponse(
        livro=LivroResponse.model_validate(db_livro.__dict__),
        capitulos=capitulos_response,
        #ideias=ideias_response
    )

