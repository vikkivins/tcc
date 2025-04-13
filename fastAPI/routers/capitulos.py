from CRUD.capitulocrud import create_capitulo, get_capitulos, get_capitulo, update_capitulo, delete_capitulo
from schemas.capituloschemas import CapituloCreate, CapituloUpdate, CapituloResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db

from model import Usuario
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
    return db_capitulo

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
