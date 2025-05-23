from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schemas.livroschemas import LivroResponse
from schemas.usuarioschemas import AutorResumoResponse

class BibliotecaResponse(BaseModel):
    livro: LivroResponse
    autor: AutorResumoResponse
    data_adicao: datetime
    
    class Config:
        orm_mode = True

class BibliotecaLivroResponse(BaseModel):
    id: int
    titulolivro: str
    descricaolivro: str
    datacriacao: datetime
    data_adicao: datetime
    autor: AutorResumoResponse
    
    class Config:
        orm_mode = True