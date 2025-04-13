from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

## LIVRO SCHEMAS

class CapituloBase(BaseModel):
    titulocapitulo: str  
    conteudocapitulo: str 
    data_criacao: datetime
    capacapitulo: Optional[str] = None 
    livro_id: int

class CapituloCreate(CapituloBase):
    pass

class CapituloUpdate(BaseModel):
    titulocapitulo: Optional[str] = None
    conteudocapitulo: Optional[str] = None
    data_criacao: Optional[datetime] = None 
    autor_ultima_modificacao: Optional[int] = None
    capacapitulo: Optional[str] = None

class CapituloResponse(CapituloBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    autor_ultima_modificacao: Optional[int] = None
    livro_id: int = None
    
    class Config:
        orm_mode = True