from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Table
from datetime import datetime, timezone  
from sqlalchemy.orm import relationship
from database import Base

# Associação entre Livro e Ideia (Relacionamento N:N)
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
    
    # Books created by this user
    livros = relationship("Livro", back_populates="usuario", foreign_keys="[Livro.usuario_id]")
    # Books modified by this user
    livros_modificados = relationship("Livro", back_populates="autor_modificacao", foreign_keys="[Livro.autor_ultima_modificacao]")
    capitulos_modificados = relationship("Capitulo", back_populates="autor_modificacao", foreign_keys="[Capitulo.autor_ultima_modificacao]")
    ideias = relationship("Ideia", back_populates="usuario")

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
    
     # Explicitly specify which foreign key to use
    usuario = relationship("Usuario", back_populates="livros", foreign_keys=[usuario_id])
    autor_modificacao = relationship("Usuario", back_populates="livros_modificados", foreign_keys=[autor_ultima_modificacao])
    capitulos = relationship("Capitulo", back_populates="livro", cascade="all, delete-orphan")
    ideias = relationship("Ideia", secondary=livro_ideia_association, back_populates="livros")
    
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
