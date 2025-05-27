from CRUD.livrocrud import create_livro, get_livros, get_livro, update_livro, delete_livro
from schemas.livroschemas import LivroCreate, LivroUpdate, LivroResponse, LivroDetalhadoResponse
from schemas.capituloschemas import CapituloResponse
from schemas.ideiaschemas import IdeiaResponse
from typing import List
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timezone

from model import Usuario, Livro, Ideia, Capitulo
from security import get_current_user

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import os


router = APIRouter(tags=['Livros'])

# Endpoints para livro
@router.post("/", response_model=LivroResponse)
def create_livro_endpoint(livro: LivroCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livro_data = livro.model_dump()
    livro_data['usuario_id'] = current_user.id
    return create_livro(db=db, **livro_data)

@router.get("/", response_model=List[LivroResponse])
def read_livros_endpoint(db: Session = Depends(get_db)):
    return get_livros(db=db)

@router.get("/minhasobras", response_model=List[LivroResponse])
def read_minhas_obras(db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livros = db.query(Livro).filter(Livro.usuario_id == current_user.id).all()
    return livros

# para que os livros sejam publicos pra quem não é autenticado
# @router.get("/publicos", response_model=List[LivroResponse])
# def read_livros_publicos_endpoint(db: Session = Depends(get_db)):
#     return db.query(Livro).filter(Livro.publico == True).all()

# Novo endpoint para livros públicos de um usuário específico
@router.get("/publicos/{username}", response_model=List[LivroResponse])
def read_livros_publicos_usuario(username: str, db: Session = Depends(get_db)):
    """Retorna apenas os livros públicos de um usuário específico"""
    # Buscar o usuário pelo username
    user = db.query(Usuario).filter(Usuario.username == username).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar apenas livros públicos deste usuário
    livros = db.query(Livro).filter(
        Livro.usuario_id == user.id,
        Livro.publico == True
    ).all()
    
    return livros

@router.put("/{livro_id}", response_model=LivroResponse)
def update_livro_endpoint(livro_id: int, livro: LivroUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    livro_data = livro.model_dump()
    livro_data['autor_ultima_modificacao'] = current_user.id
    db_livro = update_livro(db=db, livro_id=livro_id, **livro_data)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@router.delete("/{livro_id}", response_model=LivroResponse)
def delete_livro_endpoint(livro_id: int, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_livro = delete_livro(db=db, livro_id=livro_id)
    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return db_livro

@router.get("/{livro_id}", response_model=LivroDetalhadoResponse)
def read_livro_endpoint(livro_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Retorna os detalhes de um livro, incluindo:
    - Informações do livro
    - Lista de capítulos
    - Lista de ideias relacionadas (se houver)
    """
    db_livro = db.query(Livro).filter(Livro.id == livro_id).first()

    if db_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if db_livro.usuario_id != current_user.id and not db_livro.publico:
        raise HTTPException(status_code=403, detail="Acesso negado")

    capitulos = db.query(Capitulo).filter(Capitulo.livro_id == livro_id).all()
    capitulos_response = [CapituloResponse.model_validate(cap.__dict__) for cap in capitulos]


    # ideias = db.query(Ideia).filter(Ideia.livro_id == livro_id).all()
    # ideias_response = [IdeiaResponse.model_validate(ideia) for ideia in ideias]

    return LivroDetalhadoResponse(
        livro=LivroResponse.model_validate(db_livro.__dict__),
        capitulos=capitulos_response,
        #ideias=ideias_response
    )

@router.post("/{livro_id}/upload_cover")
async def upload_book_cover(
    livro_id: int,
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar se o livro existe e se o usuário tem permissão
    livro = db.query(Livro).filter(Livro.id == livro_id).first()
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    if livro.usuario_id != current_user.id:
        raise HTTPException(status_code=403, detail="Você não tem permissão para alterar a capa deste livro")
    
    # Verificar se o arquivo foi enviado
    if not file:
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado")
    
    # Configurações
    UPLOAD_FOLDER = "C:\\Users\\victo\\OneDrive\\Área de Trabalho\\tccspark\\faisca_front\\static\\uploads\\livros"
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB para capas
    
    # Verificar extensão do arquivo
    def allowed_file(filename: str) -> bool:
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Tipo de arquivo não permitido. Use PNG, JPG, JPEG, GIF ou WEBP")
    
    # Verificar tamanho do arquivo
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Arquivo muito grande (máximo 5MB)")
    
    # Criar diretório se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Gerar nome único para o arquivo
    file_ext = file.filename.split('.')[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"capa_{livro_id}_{timestamp}.{file_ext}"
    filepath = f"{UPLOAD_FOLDER}/{filename}"
    
    # Salvar arquivo
    try:
        with open(filepath, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar arquivo: {str(e)}")
    
    # Remover arquivo antigo se existir
    if livro.capalivro:
        old_filepath = os.path.join("C:\\Users\\victo\\OneDrive\\Área de Trabalho\\tccspark\\faisca_front\\static\\livros", livro.capalivro)
        if os.path.exists(old_filepath):
            try:
                os.remove(old_filepath)
            except:
                pass  # Não impedir a atualização se não conseguir remover o antigo
    
    # Atualizar banco de dados
    livro.capalivro = f"uploads/livros/{filename}"
    livro.ultima_modificacao = datetime.now(timezone.utc)
    livro.autor_ultima_modificacao = current_user.id
    db.commit()
    
    return {
        "message": "Capa do livro atualizada com sucesso", 
        "filepath": f"uploads/livros/{filename}",
        "livro_id": livro_id
    }