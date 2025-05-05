# capitulos.py (api)
from CRUD.capitulocrud import create_capitulo, get_capitulos, get_capitulo, update_capitulo, delete_capitulo
from CRUD.comentariocrud import create_comentario, get_comentarios, get_comentario, update_comentario, delete_comentario
from schemas.capituloschemas import CapituloCreate, CapituloUpdate, CapituloResponse
from schemas.comentarioschemas import ComentarioResponse, ComentarioCreate, ComentarioUpdate
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timezone

from model import Usuario, Comentario
from security import get_current_user

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix='/capitulos', tags=['capitulos'])

# Endpoints para capitulo
@router.post("/", response_model=CapituloResponse)
def create_capitulo_endpoint(capitulo: CapituloCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    capitulo_data = capitulo.model_dump()
    capitulo_data['usuario_id'] = current_user.id
    return create_capitulo(db=db, **capitulo_data)

@router.get("/{capitulo_id}", response_model=CapituloResponse)
def read_capitulo_endpoint(capitulo_id: int, db: Session = Depends(get_db)):
    db_capitulo = get_capitulo(db=db, capitulo_id=capitulo_id)
    if db_capitulo is None:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")

    comentarios = db.query(Comentario).filter(Comentario.capitulo_id == capitulo_id).all()

    # Criar um dicionário com ID -> ComentarioResponse
    comentarios_dict = {
    c.id: ComentarioResponse.model_validate({**c.__dict__, "respostas": []})
    for c in comentarios
}

    # Organizar os comentários em árvore
    comentarios_ordenados = []
    for comentario in comentarios:
        if comentario.comentario_id:
            pai = comentarios_dict.get(comentario.comentario_id)
            if pai:
                pai.respostas.append(comentarios_dict[comentario.id])
        else:
            comentarios_ordenados.append(comentarios_dict[comentario.id])

    # Adicionar os comentários principais ao capítulo  
    capitulo_dict = db_capitulo.__dict__.copy()
    capitulo_dict['comentarios'] = comentarios_ordenados

    return CapituloResponse.model_validate(capitulo_dict)


@router.get("/", response_model=List[CapituloResponse])
def read_capitulos_endpoint(db: Session = Depends(get_db)):
    return get_capitulos(db=db)

@router.put("/{capitulo_id}", response_model=CapituloResponse)
def update_capitulo_endpoint(capitulo_id: int, capitulo: CapituloUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    capitulo_data = capitulo.model_dump()
    capitulo_data['autor_ultima_modificacao'] = current_user.id
    db_capitulo = update_capitulo(db=db, capitulo_id=capitulo_id, **capitulo_data)
    if db_capitulo is None:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")
    return db_capitulo

@router.delete("/{capitulo_id}", response_model=CapituloResponse)
def delete_capitulo_endpoint(capitulo_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_capitulo = delete_capitulo(db=db, capitulo_id=capitulo_id)
    if db_capitulo is None:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")
    return db_capitulo

@router.post("/{capitulo_id}/comentarios", response_model=ComentarioResponse)
def create_comentario_endpoint(
    capitulo_id: int,
    comentario: ComentarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Verificar se o capítulo existe
    db_capitulo = get_capitulo(db=db, capitulo_id=capitulo_id)
    if db_capitulo is None:
        raise HTTPException(status_code=404, detail="Capítulo não encontrado")

    # Verificar se o comentário pai existe e pertence ao mesmo capítulo
    if comentario.comentario_id:
        comentario_pai = db.query(Comentario).filter(
            Comentario.id == comentario.comentario_id,
            Comentario.capitulo_id == capitulo_id
        ).first()
        if not comentario_pai:
            raise HTTPException(
                status_code=400,
                detail="Comentário pai não encontrado ou não pertence a este capítulo"
            )

    # Usar a função de CRUD para criar o comentário
    novo_comentario = create_comentario(
        db=db,
        datacriacao=datetime.now(timezone.utc),
        conteudocomentario=comentario.conteudocomentario,
        usuario_id=current_user.id,
        capitulo_id=capitulo_id,
        comentario_id=comentario.comentario_id,
        citacao=comentario.citacao,
        citacao_autor=comentario.citacao_autor
    )

    return novo_comentario

@router.put("/{capitulo_id}/comentarios/{comentario_id}", response_model=ComentarioResponse)
def update_comentario_endpoint(
    capitulo_id: int,
    comentario_id: int,
    comentario_update: ComentarioUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db_comentario = get_comentario(db=db, comentario_id=comentario_id)
    
    if not db_comentario or db_comentario.capitulo_id != capitulo_id:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    if db_comentario.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para editar este comentário")

    return update_comentario(db=db, comentario_id=comentario_id, conteudocomentario=comentario_update.conteudocomentario)

@router.delete("/{capitulo_id}/comentarios/{comentario_id}", response_model=ComentarioResponse)
def delete_comentario_endpoint(
    capitulo_id: int,
    comentario_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    db_comentario = get_comentario(db=db, comentario_id=comentario_id)

    if not db_comentario or db_comentario.capitulo_id != capitulo_id:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    
    if db_comentario.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para excluir este comentário")

    return delete_comentario(db=db, comentario_id=comentario_id)
