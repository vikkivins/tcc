from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from model import Usuario
from typing import Optional
import os
from datetime import datetime
from pathlib import Path
from fastapi.responses import JSONResponse

router = APIRouter(tags=['Perfil'])

# Configurações
UPLOAD_FOLDER = "C:\\Users\\victo\\OneDrive\\Área de Trabalho\\tccspark\\faisca_front\\static\\uploads\\perfil" # TODO: colocar caminho relativo 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get("/")
async def get_profile(current_user: Usuario = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "profilepic": current_user.profilepic
    }

@router.post("/upload_profile_pic")
async def upload_profile_pic(
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se o arquivo foi enviado
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    # Verificar extensão do arquivo
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido")
    
    # Verificar tamanho do arquivo
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máximo 2MB)")
    
    subfolder = "perfil"
    
    # Gerar nome único para o arquivo
    file_ext = file.filename.split('.')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"profile_{current_user.id}_{timestamp}.{file_ext}"
    #filepath = os.path.join(UPLOAD_FOLDER, filename)  # Aqui especifica a subpasta
    filepath = f"{UPLOAD_FOLDER}/{filename}"
    
    # Salvar arquivo
    try:
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")
    
    # Remover arquivo antigo se existir
    if current_user.profilepic and os.path.exists(current_user.profilepic):
        try:
            os.remove(current_user.profilepic)
        except:
            pass  # Não impedir a atualização se não conseguir remover o antigo
    
    # Atualizar banco de dados
    current_user.profilepic = f"uploads/perfil/{filename}"
    db.commit()
    
    return {"message": "Foto de perfil atualizada com sucesso", "filepath": filepath}