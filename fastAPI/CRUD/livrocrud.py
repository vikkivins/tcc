from sqlalchemy.orm import Session
from model import Livro, Capitulo
from datetime import datetime, timezone

# FUNÇÕES DE CRUD PARA LIVRO

def create_livro(db: Session, titulolivro: str, descricaolivro: str, datacriacao: str, usuario_id: int, capalivro: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    
    db_livro = Livro(titulolivro=titulolivro, descricaolivro=descricaolivro, datacriacao=datacriacao, capalivro=capalivro, usuario_id=usuario_id)
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

def get_livro(db: Session, livro_id: int):
    return db.query(Livro).filter(Livro.id == livro_id).first()

def get_livros(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Livro).offset(skip).limit(limit).all()

def update_livro(db: Session, livro_id: int, titulolivro: str = None, 
                descricaolivro: str = None, autor_ultima_modificacao: int = None, 
                capalivro: str = None, datacriacao: str = None):
    if isinstance(datacriacao, str):  # Verifica se dtnasc é string antes de converter
        datacriacao = datetime.strptime(datacriacao, '%Y-%m-%d').date()
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if db_livro:
        if titulolivro is not None: 
            db_livro.titulolivro = titulolivro
        if descricaolivro is not None: 
            db_livro.descricaolivro = descricaolivro
        if capalivro is not None: 
            db_livro.capalivro = capalivro
        if datacriacao is not None:
            db_livro.datacriacao = datacriacao
        db_livro.ultima_modificacao = datetime.now(timezone.utc)
        if autor_ultima_modificacao is not None:
            db_livro.autor_ultima_modificacao = autor_ultima_modificacao
        db.commit()
        db.refresh(db_livro)
    return db_livro

def delete_livro(db: Session, livro_id: int):
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if db_livro:
        db.query(Capitulo).filter(Capitulo.livro_id == livro_id).delete()
        db.delete(db_livro)
        db.commit()
    return db_livro