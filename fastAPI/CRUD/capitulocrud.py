from sqlalchemy.orm import Session
from model import Livro, Capitulo
from datetime import datetime, timezone

# FUNÇÕES DE CRUD PARA capitulo

def create_capitulo(db: Session, titulocapitulo: str, conteudocapitulo: str, data_criacao: str, usuario_id: int, livro_id: int, capacapitulo: str = None):
    if isinstance(data_criacao, str):  # Verifica se dtnasc é string antes de converter
        data_criacao = datetime.strptime(data_criacao, '%Y-%m-%d').date()
    
    db_capitulo = Capitulo(titulocapitulo=titulocapitulo, conteudocapitulo=conteudocapitulo, data_criacao=data_criacao, capacapitulo=capacapitulo, livro_id=livro_id, usuario_id=usuario_id)
    db.add(db_capitulo)
    db.commit()
    db.refresh(db_capitulo)
    return db_capitulo

def get_capitulo(db: Session, capitulo_id: int):
    return db.query(Capitulo).filter(Capitulo.id == capitulo_id).first()

def get_capitulos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Capitulo).offset(skip).limit(limit).all()

def update_capitulo(db: Session, capitulo_id: int, titulocapitulo: str = None, 
                conteudocapitulo: str = None, autor_ultima_modificacao: int = None, 
                capacapitulo: str = None, data_criacao: str = None):
    if isinstance(data_criacao, str):  # Verifica se dtnasc é string antes de converter
        data_criacao = datetime.strptime(data_criacao, '%Y-%m-%d').date()
    db_capitulo = db.query(Capitulo).filter(Capitulo.id == capitulo_id).first()
    if db_capitulo:
        if titulocapitulo is not None: 
            db_capitulo.titulocapitulo = titulocapitulo
        if conteudocapitulo is not None: 
            db_capitulo.conteudocapitulo = conteudocapitulo
        if capacapitulo is not None: 
            db_capitulo.capacapitulo = capacapitulo
        if data_criacao is not None:
            db_capitulo.data_criacao = data_criacao
        db_capitulo.ultima_modificacao = datetime.now(timezone.utc)
        if autor_ultima_modificacao is not None:
            db_capitulo.autor_ultima_modificacao = autor_ultima_modificacao
        db.commit()
        db.refresh(db_capitulo)
    return db_capitulo

def delete_capitulo(db: Session, capitulo_id: int):
    db_capitulo = db.query(Capitulo).filter(Capitulo.id == capitulo_id).first()
    if db_capitulo:
        db.delete(db_capitulo)
        db.commit()
    return db_capitulo