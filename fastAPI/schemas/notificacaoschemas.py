from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificacaoBase(BaseModel):
    mensagem: str
    tipo: str
    referencia_id: Optional[int] = None
    referencia_tipo: Optional[str] = None

class NotificacaoCreate(NotificacaoBase):
    usuario_id: int

class NotificacaoResponse(NotificacaoBase):
    id: int
    usuario_id: int
    data_criacao: datetime
    visualizada: bool = Field(..., alias='is_lida')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
