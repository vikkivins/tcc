from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from CRUD.notificacaocrud import criar_notificacao, listar_notificacoes, marcar_notificacao_como_lida
from schemas.usuarioschemas import UsuarioResponse
from typing import List
from model import Notification
from pydantic import BaseModel
from schemas.notificacaoschemas import NotificacaoResponse

router = APIRouter(prefix='/notificacoes', tags=['Notificacoes'])

@router.get('/{usuario_id}', response_model=List[NotificacaoResponse])
def get_notificacoes(usuario_id: int, apenas_nao_lidas: bool = False, limit: int = None, db: Session = Depends(get_db)):
    notificacoes = listar_notificacoes(db, usuario_id, apenas_nao_lidas)
    if limit:
        notificacoes = notificacoes[:limit]
    return notificacoes

@router.post('/{notificacao_id}/ler', response_model=NotificacaoResponse)
def ler_notificacao(notificacao_id: int, db: Session = Depends(get_db)):
    notificacao = marcar_notificacao_como_lida(db, notificacao_id)
    if not notificacao:
        raise HTTPException(status_code=404, detail='Notificação não encontrada')
    return notificacao
