from sqlalchemy.orm import Session
from model import Notification
from datetime import datetime, timezone

def criar_notificacao(db: Session, usuario_id: int, tipo: str, mensagem: str, referencia_id: int = None, referencia_tipo: str = None):
    notificacao = Notification(
        usuario_id=usuario_id,
        tipo=tipo,
        mensagem=mensagem,
        data_criacao=datetime.now(timezone.utc),
        is_lida=False,
        referencia_id=referencia_id,
        referencia_tipo=referencia_tipo
    )
    db.add(notificacao)
    db.commit()
    db.refresh(notificacao)
    return notificacao

def listar_notificacoes(db: Session, usuario_id: int, apenas_nao_lidas: bool = False):
    query = db.query(Notification).filter(Notification.usuario_id == usuario_id)
    if apenas_nao_lidas:
        query = query.filter(Notification.is_lida == False)
    return query.order_by(Notification.data_criacao.desc()).all()

def marcar_notificacao_como_lida(db: Session, notificacao_id: int):
    notificacao = db.query(Notification).filter(Notification.id == notificacao_id).first()
    if notificacao:
        notificacao.is_lida = True
        db.commit()
        db.refresh(notificacao)
    return notificacao
