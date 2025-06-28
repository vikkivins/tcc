from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from CRUD.usuariocrud import listar_seguidores, listar_seguindo

router = APIRouter(prefix="/followers", tags=["Followers"])

@router.get("/{usuario_id}/seguidores")
def get_seguidores(usuario_id: int, db: Session = Depends(get_db)):
    seguidores = listar_seguidores(db, usuario_id)
    return seguidores

@router.get("/{usuario_id}/seguindo")
def get_seguindo(usuario_id: int, db: Session = Depends(get_db)):
    seguindo = listar_seguindo(db, usuario_id)
    return seguindo
