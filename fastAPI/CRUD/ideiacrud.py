from sqlalchemy.orm import Session
from model import Livro, Capitulo, Ideia
from datetime import datetime, timezone

# FUNÇÕES DE CRUD PARA ideia

def create_ideia(db: Session, tituloideia: str, datacriacao: str, usuario_id: int, conteudoideia: str, capaideia: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    
    db_ideia = Ideia(tituloideia=tituloideia, datacriacao=datacriacao, conteudoideia=conteudoideia, capaideia=capaideia, usuario_id=usuario_id)
    db.add(db_ideia)
    db.commit()
    db.refresh(db_ideia)
    return db_ideia

def get_ideia(db: Session, ideia_id: int):
    return db.query(Ideia).filter(Ideia.id == ideia_id).first()

def get_ideias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Ideia).offset(skip).limit(limit).all()

def update_ideia(db: Session, ideia_id: int, tituloideia: str = None, 
                capaideia: str = None, conteudoideia: str = None, datacriacao: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    db_ideia = db.query(Ideia).filter(Ideia.id == ideia_id).first()
    if db_ideia:
        if tituloideia is not None: 
            db_ideia.tituloideia = tituloideia
        if capaideia is not None: 
            db_ideia.capaideia = capaideia
        if conteudoideia is not None:
            db_ideia.conteudoideia = conteudoideia
        if datacriacao is not None:
            db_ideia.datacriacao = datacriacao
        db_ideia.ultima_modificacao = datetime.now(timezone.utc)
        db.commit()
        db.refresh(db_ideia)
    return db_ideia

def delete_ideia(db: Session, ideia_id: int):
    db_ideia = db.query(Ideia).filter(Ideia.id == ideia_id).first()
    if db_ideia:
        db.delete(db_ideia)
        db.commit()
    return db_ideia