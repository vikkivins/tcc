from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Table, Boolean
from datetime import datetime, timezone 
from sqlalchemy.orm import relationship, backref
from database import Base

# TODO: Associação entre Livro e Ideia (Relacionamento N:N), já ta feita aqui mas falta colocar no front
livro_ideia_association = Table(
    'livro_ideia', Base.metadata,
    Column('livro_id', Integer, ForeignKey('livros.id'), primary_key=True),
    Column('ideia_id', Integer, ForeignKey('ideias.id'), primary_key=True)
)

capitulo_ideia_association = Table(
    'capitulo_ideia', Base.metadata,
    Column('capitulo_id', Integer, ForeignKey('capitulos.id'), primary_key=True),
    Column('ideia_id', Integer, ForeignKey('ideias.id'), primary_key=True)
)

biblioteca_association = Table(
    'biblioteca', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('livro_id', Integer, ForeignKey('livros.id'), primary_key=True),
    Column('data_adicao', DateTime, default=lambda: datetime.now(timezone.utc))
)

followers_association = Table(
    'followers', Base.metadata,
    Column('follower_id', Integer, ForeignKey('usuarios.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('usuarios.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    dtnasc = Column(Date, nullable=False)
    bio = Column(Text, nullable=True)
    email = Column(String(50), unique=True, nullable=False)
    senha = Column(String(60), nullable=False)
    profilepic = Column(String(50), nullable=True)
    pronome = Column(String(8), nullable=True)
    
    # Books created by this user
    livros = relationship("Livro", back_populates="usuario", foreign_keys="[Livro.usuario_id]")
    # Books modified by this user
    livros_modificados = relationship("Livro", back_populates="autor_modificacao", foreign_keys="[Livro.autor_ultima_modificacao]")
    capitulos_modificados = relationship("Capitulo", back_populates="autor_modificacao", foreign_keys="[Capitulo.autor_ultima_modificacao]")
    ideias = relationship("Ideia", back_populates="usuario")
    postagens = relationship("Postagem", back_populates="usuario")
    biblioteca = relationship("Livro", secondary=biblioteca_association, back_populates="seguidores")

    # Usuários que este usuário segue
    following = relationship(
        "Usuario",
        secondary=followers_association,
        primaryjoin=id==followers_association.c.follower_id,
        secondaryjoin=id==followers_association.c.followed_id,
        backref="followers"
    )

class Livro(Base):
    __tablename__ = 'livros'
    
    id = Column(Integer, primary_key=True, index=True)
    titulolivro = Column(String(50), nullable=False)
    descricaolivro = Column(Text, nullable=True)
    capalivro = Column(String(50), nullable=True)
    datacriacao = Column(Date, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    ultima_modificacao = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    autor_ultima_modificacao = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    publico = Column(Boolean, default=False)  # False = privado (padrão), True = público

    
    # Explicitly specify which foreign key to use
    usuario = relationship("Usuario", back_populates="livros", foreign_keys=[usuario_id])
    autor_modificacao = relationship("Usuario", back_populates="livros_modificados", foreign_keys=[autor_ultima_modificacao])
    capitulos = relationship("Capitulo", back_populates="livro", cascade="all, delete-orphan")
    ideias = relationship("Ideia", secondary=livro_ideia_association, back_populates="livros")
    seguidores = relationship("Usuario", secondary=biblioteca_association, back_populates="biblioteca")
    
class Capitulo(Base):
    __tablename__ = 'capitulos'
    
    id = Column(Integer, primary_key=True, index=True)
    titulocapitulo = Column(String(50), nullable=False)
    conteudocapitulo = Column(Text, nullable=False)
    capacapitulo = Column(String(50), nullable=True)
    livro_id = Column(Integer, ForeignKey('livros.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_criacao = Column(DateTime, nullable=False)

    ultima_modificacao = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    autor_ultima_modificacao = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    
    autor_modificacao = relationship("Usuario", back_populates="capitulos_modificados", foreign_keys=[autor_ultima_modificacao])
    livro = relationship("Livro", back_populates="capitulos")
    ideias = relationship("Ideia", secondary=capitulo_ideia_association, back_populates="capitulos")
    
class Ideia(Base):
    __tablename__ = 'ideias'
    
    id = Column(Integer, primary_key=True, index=True)
    tituloideia = Column(String(50), nullable=False)
    conteudoideia = Column(Text, nullable=False)
    capaideia = Column(String(50), nullable=True)
    datacriacao = Column(Date, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    ultima_modificacao = Column(DateTime, nullable=True, onupdate=lambda: datetime.now(timezone.utc))
    
    usuario = relationship("Usuario", back_populates="ideias")
    livros = relationship("Livro", secondary=livro_ideia_association, back_populates="ideias")
    capitulos = relationship("Capitulo", secondary=capitulo_ideia_association, back_populates="ideias")

class Comentario(Base):
    __tablename__='comentarios'

    id = Column(Integer, primary_key=True, index=True)
    datacriacao = Column(DateTime, nullable=False)
    conteudocomentario = Column(Text, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    capitulo_id = Column(Integer, ForeignKey('capitulos.id'), nullable=False)
    comentario_id = Column(Integer, ForeignKey('comentarios.id'), nullable=True)
    
    citacao = Column(Text, nullable=True)
    citacao_autor = Column(String(255), nullable=True)

    usuario = relationship("Usuario")
    capitulo = relationship("Capitulo")
    respostas = relationship(
        "Comentario",
        backref=backref('pai', remote_side=[id]),
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

class Postagem(Base):
    __tablename__='postagens'

    id = Column(Integer, primary_key=True, index=True)
    datacriacao = Column(DateTime, nullable=False)
    conteudopostagem = Column(Text, nullable=False)
    postagem_id = Column(Integer, ForeignKey('postagens.id'), nullable=True) # caso haja um post pai
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="postagens")
    
class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)  # Quem recebe a notificação
    tipo = Column(String(30), nullable=False)  # Ex: novo_seguidor, nova_postagem, novo_livro, novo_capitulo
    mensagem = Column(Text, nullable=False)
    data_criacao = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_lida = Column(Boolean, default=False)
    referencia_id = Column(Integer, nullable=True)  # ID do objeto relacionado
    referencia_tipo = Column(String(30), nullable=True)  # Tipo do objeto relacionado

    usuario = relationship('Usuario')