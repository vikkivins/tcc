from sqlalchemy.orm import Session
from database import get_db
from model import Usuario
from security import verify_password, create_access_token
from schemas.tokenschemas import Token
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/login', tags=['Login'])

#### ENDPOINT LOGIN

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Debug: mostra as credenciais recebidas
    print(f"Tentativa de login com username: {form_data.username}")
    
    usuario = db.query(Usuario).filter(Usuario.username == form_data.username).first()
    
    if not usuario:
        print("Usuário não encontrado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    test_hash = bcrypt.hashpw(form_data.password.encode('utf-8'), usuario.senha.encode('utf-8'))
    print(f"Test hash: {test_hash.decode('utf-8')}")
    print(f"Comparando: {test_hash.decode('utf-8') == usuario.senha}")
    
    # Debug: mostra os valores que serão comparados
    print(f"Comparando senha fornecida: '{form_data.password}'")
    print(f"Com hash armazenado: '{usuario.senha}'")
    
    # Verifica a senha
    if not verify_password(form_data.password, usuario.senha):
        print("Falha na verificação da senha")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Gera o token de acesso
    access_token = create_access_token(
        data={"sub": usuario.username, "user_id": usuario.id}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}