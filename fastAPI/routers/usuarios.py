from CRUD.usuariocrud import create_usuario, get_usuario, get_usuarios, update_usuario, delete_usuario, seguir_usuario, deixar_de_seguir_usuario
from CRUD.notificacaocrud import criar_notificacao
from schemas.usuarioschemas import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from model import Usuario
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(prefix='/usuarios', tags=['Usuarios'])

# Endpoints para Usuario
@router.post("/", response_model=UsuarioResponse)
def create_usuario_endpoint(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar se o email já existe
    existing_email = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já está em uso por outro usuário"
        )
    
    # Verificar se o username já existe
    existing_username = db.query(Usuario).filter(Usuario.username == usuario.username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username já está em uso por outro usuário"
        )
    
    # Se tudo estiver ok, criar o usuário
    return create_usuario(db=db, **usuario.model_dump())

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def read_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = get_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.get("/", response_model=List[UsuarioResponse])
def read_usuarios_endpoint(db: Session = Depends(get_db), username: str = None):
    if username:
        usuarios = db.query(Usuario).filter(Usuario.username == username).all()
        return usuarios
    return get_usuarios(db=db)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario_endpoint(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = update_usuario(db=db, usuario_id=usuario_id, **usuario.model_dump())
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.delete("/{usuario_id}", response_model=UsuarioResponse)
def delete_usuario_endpoint(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = delete_usuario(db=db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_usuario

@router.post("/{follower_id}/seguir/{followed_id}")
def seguir(follower_id: int, followed_id: int, db: Session = Depends(get_db)):
    result = seguir_usuario(db, follower_id, followed_id)
    # Notificação: novo seguidor
    from model import Usuario
    follower = db.query(Usuario).filter(Usuario.id == follower_id).first()
    if follower:
        criar_notificacao(
            db,
            usuario_id=followed_id,
            tipo="novo_seguidor",
            mensagem=f"{follower.username} começou a te seguir.",
            referencia_id=follower_id,
            referencia_tipo="usuario"
        )
    return result

@router.post("/{follower_id}/deixar_de_seguir/{followed_id}")
def deixar_de_seguir(follower_id: int, followed_id: int, db: Session = Depends(get_db)):
    return deixar_de_seguir_usuario(db, follower_id, followed_id)