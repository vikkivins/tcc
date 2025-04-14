from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from security import get_current_user
from model import Usuario, Livro
from schemas.livroschemas import LivroResponse
from typing import List

from schemas.livroschemas import LivroComAutorResponse
from schemas.usuarioschemas import AutorResumoResponse
from CRUD.usuariocrud import get_usuario

router = APIRouter(prefix='/explorar', tags=['Explorar'])

@router.get("/explorar", response_model=List[LivroComAutorResponse])
async def get_explorar_data(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    livros_publicos = (
        db.query(Livro)
        .filter(Livro.publico == True, Livro.usuario_id != current_user.id)
        .all()
    )

    resposta = []
    for livro in livros_publicos:
        autor = get_usuario(db, livro.usuario_id)
        resposta.append(
            LivroComAutorResponse(
                livro=LivroResponse.model_validate(livro.__dict__),
                autor=AutorResumoResponse.model_validate(autor.__dict__)
            )
        )

    return resposta
