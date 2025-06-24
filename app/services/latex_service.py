# NOVO ARQUIVO: app/services/latex_service.py
import os
import subprocess
import tempfile
import shutil
from fastapi import HTTPException, status

def compile_latex_to_pdf(latex_code: str) -> bytes:
    """
    Compila uma string de código LaTeX para um arquivo PDF e retorna os bytes do PDF.
    Cria um diretório temporário para lidar com os arquivos de compilação.
    """
    # Cria um diretório temporário seguro
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Define os caminhos para os arquivos .tex e .pdf
        tex_file_path = os.path.join(temp_dir, 'slide.tex')
        pdf_file_path = os.path.join(temp_dir, 'slide.pdf')

        # Escreve o código LaTeX recebido no arquivo .tex
        with open(tex_file_path, 'w', encoding='utf-8') as f:
            f.write(latex_code)

        # Comando para compilar o .tex para .pdf usando pdflatex
        # O pdflatex é executado duas vezes para garantir que todas as referências (ex: sumário) sejam resolvidas
        command = [
            'pdflatex',
            '-interaction=nonstopmode', # Não para em erros, tenta continuar
            '-output-directory=' + temp_dir,
            tex_file_path
        ]
        
        # Executa o comando de compilação
        for i in range(2): # Roda duas vezes
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode != 0:
                # Se a compilação falhar, lança uma exceção com o log de erro
                error_log = process.stdout or process.stderr
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Erro na compilação do LaTeX. Log: {error_log}"
                )

        # Verifica se o PDF foi realmente criado
        if not os.path.exists(pdf_file_path):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A compilação do LaTeX pareceu bem-sucedida, mas o arquivo PDF não foi encontrado."
            )

        # Lê os bytes do arquivo PDF gerado
        with open(pdf_file_path, 'rb') as f:
            pdf_bytes = f.read()
            
        return pdf_bytes

    finally:
        # Garante que o diretório temporário e todo o seu conteúdo sejam removidos
        shutil.rmtree(temp_dir)