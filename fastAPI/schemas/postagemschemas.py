from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

## POSTAGEM SCHEMAS

class PostagemBase(BaseModel):  
    conteudopostagem: str 
    data_criacao: datetime
    postagem_id: int

class PostagemCreate(PostagemBase):
    pass

class PostagemUpdate(BaseModel):
    conteudopostagem: Optional[str] = None
    data_criacao: Optional[datetime] = None

class PostagemResponse(PostagemBase):
    id: int
    usuario_id: int
    ultima_modificacao: Optional[datetime] = None
    postagem_id: int = None
    
    class Config:
        orm_mode = True