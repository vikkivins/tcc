from sqlalchemy.orm import Session
from model import Comentario
from datetime import datetime, timezone

# FUNÇÕES DE CRUD PARA comentario
# conteudocomentario: str 
#     data_criacao: datetime
#     capitulo_id: int
#     comentario_id: int

def create_comentario(db: Session, datacriacao: str, conteudocomentario: str, usuario_id: int, capitulo_id: int, comentario_id: int):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    
    db_comentario = Comentario(datacriacao=datacriacao, conteudocomentario=conteudocomentario, usuario_id=usuario_id, capitulo_id=capitulo_id, comentario_id=comentario_id)
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def get_comentario(db: Session, comentario_id: int):
    return db.query(Comentario).filter(Comentario.id == comentario_id).first()

def get_comentarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Comentario).offset(skip).limit(limit).all()

def update_comentario(db: Session, comentario_id: int, conteudocomentario: str = None, datacriacao: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario:
        if conteudocomentario is not None:
            db_comentario.conteudocomentario = conteudocomentario
        if datacriacao is not None:
            db_comentario.datacriacao = datacriacao
        db_comentario.ultima_modificacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_comentario)
    return db_comentario

def delete_comentario(db: Session, comentario_id: int):
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario:
        db.delete(db_comentario)
        db.commit()
    return db_comentario