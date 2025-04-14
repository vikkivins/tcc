from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

from schemas.ideiaschemas import IdeiaResponse
from schemas.capituloschemas import CapituloResponse

## LIVRO SCHEMAS

class LivroBase(BaseModel):
    titulolivro: str  
    descricaolivro: str 
    datacriacao: date  
    capalivro: Optional[str] = None 
    publico: Optional[bool] = False  # novo campo

class LivroCreate(LivroBase):
    pass

class LivroUpdate(BaseModel):
    titulolivro: Optional[str] = None
    descricaolivro: Optional[str] = None
    datacriacao: Optional[date] = None 
    autor_ultima_modificacao: Optional[int] = None
    capalivro: Optional[str] = None
    publico: Optional[bool] = None

class LivroResponse(LivroBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    autor_ultima_modificacao: Optional[int] = None
    
    class Config:
        orm_mode = True

class LivroDetalhadoResponse(BaseModel):
    livro: LivroResponse
    capitulos: List[CapituloResponse] = []
    ideias: List[IdeiaResponse] = []

from schemas.usuarioschemas import AutorResumoResponse

class LivroComAutorResponse(BaseModel):
    livro: LivroResponse
    autor: AutorResumoResponse