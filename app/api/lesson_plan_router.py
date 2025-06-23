# Em: app/api/lesson_plan_router.py
from typing import List # Importa List para tipagem de listas
from fastapi import APIRouter, Depends # Importa o APIRouter para criar rotas
from sqlalchemy.orm import Session # Importa o Session para interagir com o banco de dados
from app.models import schemas # Importa nossos schemas para validação de dados
from app.services import ia_service # Importa nosso serviço de IA para gerar planos de aula
from app.database import get_db # Importa nossa nova dependência
from fastapi import APIRouter, Depends, Response, HTTPException, status # Importa o APIRouter, Depends e outras classes necessárias
from app.services import pdf_service # Importar o nosso novo serviço de PDF
from app.api.auth_router import get_current_user # Importa a função para obter o usuário atual (se necessário)

router = APIRouter()

@router.post("/generate/lesson_plan", name="Gerar Plano de Aula")
def generate_lesson_plan(
    request_data: schemas.LessonPlanRequest, 
    db: Session = Depends(get_db), # <-- Injeta a sessão do banco na nossa função
    current_user: schemas.UserOut = Depends(get_current_user) # <-- Injeta o usuário atual
):
    """
    Gera os planos de aula com a IA e salva no banco de dados.
    """
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
        content=plano_de_aula_real,
        owner_id=current_user.id  # <-- PEGA O ID DO USUÁRIO A PARTIR DO TOKEN!
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

@router.get("/lesson_plans/", response_model=List[schemas.LessonPlanInList])
def get_user_lesson_plans(
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user) # Protege a rota!
):
    """
    Retorna uma lista de todos os planos de aula
    pertencentes ao usuário atualmente logado.
    """
    # Faz a busca no banco por todos os planos cujo owner_id é o do usuário logado
    plans = db.query(schemas.LessonPlan).filter(schemas.LessonPlan.owner_id == current_user.id).all()
    
    return plans

@router.get("/{plan_id}/download")
def download_lesson_plan_pdf(plan_id: int, 
                             db: Session = Depends(get_db),
                             current_user: schemas.UserOut = Depends(get_current_user)):
    """
    Permite que o usuário baixe um plano de aula específico
    em formato PDF, gerando o PDF a partir do conteúdo Markdown.
    """
    # 1. Busca o plano de aula no banco de dados pelo ID fornecido
    db_plan = db.query(schemas.LessonPlan).filter(schemas.LessonPlan.id == plan_id).first()

    if not db_plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de aula não encontrado ou você não tem permissão para acessá-lo."
        )
    
    # 2. Usa nosso novo serviço para gerar os bytes do PDF a partir do conteúdo Markdown
    pdf_bytes = pdf_service.criar_pdf_do_markdown(db_plan.content) # type: ignore
    
    # 3. Cria um nome de arquivo dinâmico
    file_name = f"plano_de_aula_{db_plan.topic.replace(' ', '_').lower()}.pdf"
    
    # 4. Define os headers para o download do PDF
    headers = {
        'Content-Disposition': f'inline; filename="{file_name}"'
    }

    # 5. Retorna o PDF como uma resposta de download
    return Response(
        content=pdf_bytes,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename={file_name}'}
    )

@router.delete("/{plan_id}/delete", status_code=status.HTTP_200_OK)
def delete_lesson_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserOut = Depends(get_current_user)
):
    """
    Deleta um plano de aula específico.
    Apenas o dono do plano de aula pode deletá-lo.
    """
    # Busca o plano no banco para garantir que ele existe E pertence ao usuário logado
    plan_to_delete = db.query(schemas.LessonPlan).filter(
        schemas.LessonPlan.id == plan_id,
        schemas.LessonPlan.owner_id == current_user.id
    ).first()

    # Se a busca não encontrar nada, significa que o plano não existe ou não é do usuário
    if not plan_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano de aula não encontrado ou você não tem permissão para esta ação."
        )
    
    # Se encontrou, deleta o plano do banco de dados
    db.delete(plan_to_delete)
    db.commit()
    
    return {"detail": f"Plano de aula com ID {plan_id} deletado com sucesso."}