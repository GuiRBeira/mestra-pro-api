# Em: app/services/pdf_service.py

from markdown_it import MarkdownIt
from weasyprint import HTML

def criar_pdf_do_markdown(markdown_string: str) -> bytes:
    """
    Converte uma string de texto em formato Markdown para um arquivo PDF em memória.
    Retorna os bytes do PDF gerado.
    """
    # Inicializa o conversor de Markdown
    md = MarkdownIt()
    
    # Converte a string de Markdown para uma string de HTML
    html_string = md.render(markdown_string)
    
    # WeasyPrint pega o HTML e "imprime" em um PDF, retornando os bytes
    pdf_bytes = HTML(string=html_string).write_pdf()
    
    return pdf_bytes