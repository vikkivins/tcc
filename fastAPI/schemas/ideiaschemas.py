from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

## Ideia SCHEMAS

class IdeiaBase(BaseModel):
    tituloideia: str  
    conteudoideia: str 
    datacriacao: date
    capaideia: Optional[str] = None 

class IdeiaCreate(IdeiaBase):
    pass

class IdeiaUpdate(BaseModel):
    tituloideia: Optional[str] = None
    conteudoideia: Optional[str] = None
    datacriacao: Optional[date] = None 
    capaideia: Optional[str] = None

class IdeiaResponse(IdeiaBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    livro_id: int = None
    capitulo_id: int = None
    
    class Config:
        orm_mode = True