from sqlalchemy.orm import Session
from sqlalchemy import and_
from model import Usuario, Livro, biblioteca_association
from datetime import datetime, timezone
from typing import List

def adicionar_livro_biblioteca(db: Session, usuario_id: int, livro_id: int):
    """Adiciona um livro à biblioteca do usuário"""
    # Verificar se o livro já está na biblioteca
    existing = db.execute(
        biblioteca_association.select().where(
            and_(
                biblioteca_association.c.usuario_id == usuario_id,
                biblioteca_association.c.livro_id == livro_id
            )
        )
    ).first()
    
    if existing:
        return False 
    
    # Adicionar à biblioteca
    stmt = biblioteca_association.insert().values(
        usuario_id=usuario_id,
        livro_id=livro_id,
        data_adicao=datetime.now(timezone.utc)
    )
    db.execute(stmt)
    db.commit()
    return True

def remover_livro_biblioteca(db: Session, usuario_id: int, livro_id: int):
    """Remove um livro da biblioteca do usuário"""
    stmt = biblioteca_association.delete().where(
        and_(
            biblioteca_association.c.usuario_id == usuario_id,
            biblioteca_association.c.livro_id == livro_id
        )
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0

def get_biblioteca_usuario(db: Session, usuario_id: int):
    """Retorna todos os livros da biblioteca do usuário"""
    query = db.query(Livro, Usuario, biblioteca_association.c.data_adicao)\
        .join(biblioteca_association, Livro.id == biblioteca_association.c.livro_id)\
        .join(Usuario, Livro.usuario_id == Usuario.id)\
        .filter(biblioteca_association.c.usuario_id == usuario_id)\
        .order_by(biblioteca_association.c.data_adicao.desc())
    
    return query.all()

def verificar_livro_na_biblioteca(db: Session, usuario_id: int, livro_id: int):
    """Verifica se um livro está na biblioteca do usuário"""
    result = db.execute(
        biblioteca_association.select().where(
            and_(
                biblioteca_association.c.usuario_id == usuario_id,
                biblioteca_association.c.livro_id == livro_id
            )
        )
    ).first()
    return result is not None