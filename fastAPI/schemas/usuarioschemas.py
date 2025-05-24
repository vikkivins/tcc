from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

### USUARIO SCHEMAS

# Modelo de resposta do usuário
class UsuarioBase(BaseModel):
    nome: str  
    username: str 
    dtnasc: date  
    bio: Optional[str] = None 
    email: EmailStr
    senha: str
    profilepic: Optional[str] = None
    pronome: Optional[str] = None

# Modelo para criação de usuário (com todos os campos necessários para criação)
class UsuarioCreate(UsuarioBase):
    pass  # Nenhuma alteração necessária aqui, pois a criação usa os mesmos campos

# Modelo para atualização de usuário (todos os campos são opcionais para atualização)
class UsuarioUpdate(UsuarioBase):
    nome: Optional[str] = None
    username: Optional[str] = None
    dtnasc: Optional[date] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    profilepic: Optional[str] = None
    pronome: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    
    class Config:
        orm_mode = True

class AutorResumoResponse(BaseModel):
    username: str
    profilepic: Optional[str] = None

    class Config:
        orm_mode = True
