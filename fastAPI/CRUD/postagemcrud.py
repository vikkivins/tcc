from sqlalchemy.orm import Session
from model import Postagem
from datetime import datetime, timezone

# FUNÇÕES DE CRUD PARA postagem
# id = Column(Integer, primary_key=True, index=True)
#     datacriacao = Column(DateTime, nullable=False)
#     conteudopostagem = Column(Text, nullable=False)
#     postagem_id = Column(Integer, ForeignKey('postagens.id'), nullable=True)

def create_postagem(db: Session, datacriacao: str, conteudopostagem: str, usuario_id: int, postagem_id: int = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d - %H:%M').date()

    db_postagem = Postagem(datacriacao=datacriacao, conteudopostagem=conteudopostagem, usuario_id=usuario_id, postagem_id=postagem_id)
    db.add(db_postagem)
    db.commit()
    db.refresh(db_postagem)
    return db_postagem

def get_postagem(db: Session, postagem_id: int):
    return db.query(Postagem).filter(Postagem.id == postagem_id).first()

def get_postagens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Postagem).offset(skip).limit(limit).all()

def update_postagem(db: Session, postagem_id: int, conteudopostagem: str = None, datacriacao: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d - %H:%M').date()
    db_postagem = db.query(Postagem).filter(Postagem.id == postagem_id).first()
    if db_postagem:
        if conteudopostagem is not None:
            db_postagem.conteudopostagem = conteudopostagem
        if datacriacao is not None:
            db_postagem.datacriacao = datacriacao
        db_postagem.ultima_modificacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_postagem)
    return db_postagem

def delete_postagem(db: Session, postagem_id: int):
    db_postagem = db.query(Postagem).filter(Postagem.id == postagem_id).first()
    if db_postagem:
        db.delete(db_postagem)
        db.commit()
    return db_postagem