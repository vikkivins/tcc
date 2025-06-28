from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from database import get_db
from security import get_current_user
from model import Usuario, Postagem
from schemas.postagemschemas import PostagemCreate, PostagemUpdate, PostagemResponse
from CRUD import postagemcrud
from CRUD.notificacaocrud import criar_notificacao

router = APIRouter(prefix="/postagens", tags=["Postagens"])

# 📌 Listar postagens (excluindo as do usuário atual, por padrão)
@router.get("/", response_model=List[PostagemResponse])
async def listar_postagens(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    postagens = (
        db.query(Postagem)
        .order_by(Postagem.datacriacao.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return postagens

# Listar MINHAS postagens

@router.get("/minhasatualizacoes", response_model=List[PostagemResponse])
async def listar_minhas_postagens(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    postagens = (
        db.query(Postagem)
        .filter(Postagem.usuario_id == current_user.id)
        .order_by(Postagem.datacriacao.desc())
        .all()
    )
    return postagens

@router.get("/{username}", response_model=List[PostagemResponse])
def read_postagens_usuario(
    username: str, 
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Retorna as postagens de um usuário específico"""
    
    # Buscar o usuário pelo username
    user = db.query(Usuario).filter(Usuario.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    postagens = db.query(Postagem).filter(
        Postagem.usuario_id == user.id
    ).order_by(Postagem.datacriacao.desc()).all()
    
    return postagens


# 🆕 Criar uma nova postagem
@router.post("/", response_model=PostagemResponse)
async def criar_postagem(
    postagem: PostagemCreate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    nova_postagem = postagemcrud.create_postagem(
        db=db,
        datacriacao=datetime.now(timezone.utc),
        conteudopostagem=postagem.conteudopostagem,
        usuario_id=current_user.id,
        postagem_id=postagem.postagem_id
    )
    # Notificar seguidores do autor
    autor = db.query(Usuario).filter(Usuario.id == current_user.id).first()
    if autor and hasattr(autor, 'followers'):
        for seguidor in autor.followers:
            criar_notificacao(
                db,
                usuario_id=seguidor.id,
                tipo="nova_postagem",
                mensagem=f"{autor.username} fez uma nova postagem.",
                referencia_id=nova_postagem.id,
                referencia_tipo="postagem"
            )
    return nova_postagem

# ✏️ Atualizar uma postagem
@router.put("/{postagem_id}", response_model=PostagemResponse)
async def atualizar_postagem(
    postagem_id: int,
    postagem: PostagemUpdate,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_postagem = postagemcrud.get_postagem(db, postagem_id)
    if not db_postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")
    if db_postagem.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar esta postagem")
    
    postagem_atualizada = postagemcrud.update_postagem(
        db=db,
        postagem_id=postagem_id,
        conteudopostagem=postagem.conteudopostagem,
        datacriacao=postagem.datacriacao
    )
    return postagem_atualizada

# ❌ Deletar uma postagem
@router.delete("/{postagem_id}", response_model=PostagemResponse)
async def deletar_postagem(
    postagem_id: int,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_postagem = postagemcrud.get_postagem(db, postagem_id)
    if not db_postagem:
        raise HTTPException(status_code=404, detail="Postagem não encontrada")
    if db_postagem.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para deletar esta postagem")

    postagem_excluida = postagemcrud.delete_postagem(db, postagem_id)
    return postagem_excluida
