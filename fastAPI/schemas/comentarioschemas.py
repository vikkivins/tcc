from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

## COMENTARIO SCHEMAS

class ComentarioBase(BaseModel):  
    conteudocomentario: str 
    data_criacao: datetime
    capitulo_id: int
    comentario_id: int

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(BaseModel):
    conteudocomentario: Optional[str] = None
    data_criacao: Optional[datetime] = None

class ComentarioResponse(ComentarioBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    capitulo_id: int = None
    comentario_id: int = None
    
    class Config:
        orm_mode = True