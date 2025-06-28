from sqlalchemy.orm import Session
from model import Usuario, Livro, Capitulo, Ideia
from datetime import datetime
from security import get_password_hash
from fastapi import HTTPException, status

# FUNÇÕES DE CRUD PARA USUÁRIO
def create_usuario(db: Session, nome: str, username: str, dtnasc: str, email: str, senha: str, bio: str = None, profilepic: str = None,
                   pronome: str = None):
    # Debug: Mostra a senha recebida
    print(f"Senha recebida no cadastro: {senha}")
    
    # Verifica se já existe usuário com mesmo email ou username
    existing_user = db.query(Usuario).filter(
        (Usuario.email == email) | (Usuario.username == username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ou username já cadastrado"
        )
    
    # Gera o hash da senha
    hashed_password = get_password_hash(senha)
    print(f"Hash gerado: {hashed_password}")
    if isinstance(dtnasc, str):  # Verifica se dtnasc é string antes de converter
        dtnasc = datetime.strptime(dtnasc, '%Y-%m-%d').date()
    # Cria o novo usuário
    db_usuario = Usuario(
        nome=nome,
        username=username,
        dtnasc=dtnasc,
        email=email,
        senha=hashed_password,  # Armazena o hash, não a senha plain text
        bio=bio,
        profilepic=profilepic,
        pronome=pronome
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def get_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def update_usuario(db: Session, usuario_id: int, nome: str = None, username: str = None, dtnasc: str = None, email: str = None, 
                   senha: str = None, bio: str = None, profilepic: str = None, pronome: str = None):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        if nome: db_usuario.nome = nome
        if username: db_usuario.username = username
        if dtnasc: db_usuario.dtnasc = dtnasc
        if email: db_usuario.email = email
        if senha: db_usuario.senha = get_password_hash(senha)
        if bio: db_usuario.bio = bio
        if profilepic: db_usuario.profilepic = profilepic
        if pronome: db_usuario.pronome = pronome
        db.commit()
        db.refresh(db_usuario)
    return db_usuario

def delete_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario:
        db.query(Ideia).filter(Ideia.usuario_id == usuario_id).delete()
        db.query(Livro).filter(Livro.usuario_id == usuario_id).delete()
        db.delete(db_usuario)
        db.commit()
    return db_usuario

def seguir_usuario(db: Session, follower_id: int, followed_id: int):
    from model import Usuario, followers_association
    if follower_id == followed_id:
        raise HTTPException(status_code=400, detail="Você não pode seguir a si mesmo.")
    follower = db.query(Usuario).filter(Usuario.id == follower_id).first()
    followed = db.query(Usuario).filter(Usuario.id == followed_id).first()
    if not follower or not followed:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if followed in follower.following:
        raise HTTPException(status_code=400, detail="Usuário já seguido.")
    follower.following.append(followed)
    db.commit()
    return {"msg": f"Usuário {follower.username} agora segue {followed.username}"}

def deixar_de_seguir_usuario(db: Session, follower_id: int, followed_id: int):
    from model import Usuario
    follower = db.query(Usuario).filter(Usuario.id == follower_id).first()
    followed = db.query(Usuario).filter(Usuario.id == followed_id).first()
    if not follower or not followed:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if followed not in follower.following:
        raise HTTPException(status_code=400, detail="Usuário não está sendo seguido.")
    follower.following.remove(followed)
    db.commit()
    return {"msg": f"Usuário {follower.username} deixou de seguir {followed.username}"}

def listar_seguidores(db: Session, usuario_id: int):
    from model import Usuario
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario.followers

def listar_seguindo(db: Session, usuario_id: int):
    from model import Usuario
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return usuario.following

