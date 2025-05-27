from fastapi import FastAPI
from database import engine
from model import Base

from routers import usuarios, livros, login, biblioteca, capitulos, ideias, explorar, postagens, perfil

# Criando as tabelas no banco de dados com base nos modelos
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(usuarios.router)
app.include_router(livros.router, prefix="/livros")
app.include_router(ideias.router)
app.include_router(capitulos.router)
app.include_router(login.router)
app.include_router(biblioteca.router, prefix="/biblioteca")
app.include_router(explorar.router)
app.include_router(postagens.router)
app.include_router(perfil.router, prefix="/perfil")