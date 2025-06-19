# Em: app/api/lesson_plan_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import schemas
from app.services import ia_service
from app.database import get_db # Importa nossa nova dependência

router = APIRouter()

@router.post("/generate/lesson_plan", name="Gerar Plano de Aula")
def generate_lesson_plan(
    request_data: schemas.LessonPlanRequest, 
    db: Session = Depends(get_db) # <-- Injeta a sessão do banco na nossa função
):
    # 1. Chama a IA para gerar o conteúdo (código que você já tem)
    plano_de_aula_real = ia_service.gerar_plano_de_aula_com_ia(
        topic=request_data.topic,
        grade=request_data.grade,
        subject=request_data.subject
    )

    # --- LÓGICA NOVA PARA SALVAR NO BANCO ---
    # 2. Cria um objeto do nosso modelo de tabela com os dados
    novo_plano_db = schemas.LessonPlan(
        topic=request_data.topic,
        grade=request_data.grade,
        subject=request_data.subject,
        content=plano_de_aula_real
    )
    # 3. Adiciona o novo objeto à sessão do banco de dados
    db.add(novo_plano_db)
    # 4. Confirma a transação, salvando os dados de verdade
    db.commit()
    # 5. Atualiza o objeto com os dados que o banco gerou (como o ID)
    db.refresh(novo_plano_db)
    # ----------------------------------------

    # 6. Retorna o plano gerado para o front-end
    return {"plan": plano_de_aula_real}