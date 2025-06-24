# app/api/beamer_router.py
from fastapi import APIRouter, Depends, Response, HTTPException, status
from app.models import schemas
from app.services import latex_service, ia_service # Adiciona ia_service
from app.api.auth_router import get_current_user

router = APIRouter()

# --- NOVA ROTA ---
@router.post("/generate/beamer_from_plan", response_model=schemas.LatexRequest, name="Gerar Código Beamer com IA")
def generate_beamer_code_from_plan(
    request: schemas.LessonPlanContent,
    current_user: schemas.UserOut = Depends(get_current_user)
):
    """
    Recebe o conteúdo de um plano de aula e usa a IA para gerar o código LaTeX Beamer.
    """
    try:
        latex_code = ia_service.gerar_beamer_com_ia(request.content)
        return {"latex_code": latex_code}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao gerar o código LaTeX com a IA: {str(e)}"
        )


@router.post("/generate/beamer_pdf", name="Gerar PDF de Slides Beamer")
def generate_beamer_pdf(
    request: schemas.LatexRequest,
    current_user: schemas.UserOut = Depends(get_current_user) # Protege a rota
):
    """
    Recebe um código LaTeX, compila-o para PDF e retorna o arquivo para download.
    """
    try:
        # Chama o serviço para compilar o LaTeX e obter os bytes do PDF
        pdf_bytes = latex_service.compile_latex_to_pdf(request.latex_code)

        # Prepara os headers para a resposta de download
        headers = {
            'Content-Disposition': 'attachment; filename="slides_mestrapro.pdf"'
        }

        # Retorna a resposta com o conteúdo do PDF
        return Response(
            content=pdf_bytes,
            media_type='application/pdf',
            headers=headers
        )
    except HTTPException as e:
        # Re-lança exceções HTTP geradas pelo serviço (ex: erro de compilação)
        raise e
    except Exception as e:
        # Captura outras exceções inesperadas
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro inesperado no servidor: {str(e)}"
        )