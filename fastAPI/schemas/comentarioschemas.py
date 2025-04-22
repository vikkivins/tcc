from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

## COMENTARIO SCHEMAS

class ComentarioBase(BaseModel):  
    conteudocomentario: str 
    datacriacao: datetime
    capitulo_id: int
    comentario_id: Optional[int] = None

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(BaseModel):
    conteudocomentario: Optional[str] = None
    datacriacao: Optional[datetime] = None

class ComentarioResponse(ComentarioBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    capitulo_id: int = None
    comentario_id: Optional[int] = None
    respostas: List["ComentarioResponse"] = []

    class Config:
        orm_mode = True

ComentarioResponse.model_rebuild()