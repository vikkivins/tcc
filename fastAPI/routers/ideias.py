from CRUD.ideiacrud import create_ideia, get_ideias, get_ideia, update_ideia, delete_ideia
from schemas.ideiaschemas import IdeiaCreate, IdeiaUpdate, IdeiaResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db

from model import Usuario, Ideia
from security import get_current_user

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix='/ideias', tags=['ideias'])

# Endpoints para ideia
@router.post("/", response_model=IdeiaResponse)
def create_ideia_endpoint(ideia: IdeiaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    ideia_data = ideia.model_dump()
    ideia_data['usuario_id'] = current_user.id
    return create_ideia(db=db, **ideia_data)

@router.get("/", response_model=List[IdeiaResponse])
def read_ideias_endpoint(db: Session = Depends(get_db)):
    return get_ideias(db=db)

@router.put("/{ideia_id}", response_model=IdeiaResponse)
def update_ideia_endpoint(ideia_id: int, ideia: IdeiaUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    ideia_data = ideia.model_dump()
    db_ideia = update_ideia(db=db, ideia_id=ideia_id, **ideia_data)
    if db_ideia is None:
        raise HTTPException(status_code=404, detail="ideia não encontrada")
    return db_ideia

@router.delete("/{ideia_id}", response_model=IdeiaResponse)
def delete_ideia_endpoint(ideia_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_ideia = delete_ideia(db=db, ideia_id=ideia_id)
    if db_ideia is None:
        raise HTTPException(status_code=404, detail="ideia não encontrada")
    return db_ideia

@router.get("/{ideia_id}", response_model=IdeiaResponse)
def read_ideia_endpoint(ideia_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Retorna os detalhes de uma ideia específica.
    """
    db_ideia = db.query(Ideia).filter(Ideia.id == ideia_id).first()

    if db_ideia is None:
        raise HTTPException(status_code=404, detail="Ideia não encontrada")

    if db_ideia.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return db_ideia
