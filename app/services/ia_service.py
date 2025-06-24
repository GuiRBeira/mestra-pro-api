# Em: app/services/ia_service.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura a API key a partir da variável de ambiente
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("A chave da API do Google não foi encontrada. Verifique seu arquivo .env")

genai.configure(api_key=api_key)

# Configura o modelo generativo que vamos usar
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def gerar_plano_de_aula_com_ia(topic: str, grade: str, subject: str) -> str:
    """
    Monta um prompt e envia para a API do Gemini para gerar um plano de aula.
    """
    # Este é o prompt, a "ordem" que damos para a IA.
    prompt = f"""
    Atue como um especialista em pedagogia e criação de conteúdo educacional.
    Sua tarefa é criar um plano de aula detalhado e bem estruturado.
    O formato da resposta deve ser em Markdown.
    **Tema da Aula:** {topic}
    **Disciplina:** {subject}
    **Série/Ano:** {grade}

    O plano de aula deve conter as seguintes seções obrigatórias:
    1.  **Objetivos de Aprendizagem:** Liste 3 objetivos claros e mensuráveis.
    2.  **Conteúdo Programático:** Detalhe os tópicos e sub-tópicos a serem abordados.
    3.  **Metodologia de Ensino:** Descreva as etapas da aula (ex: introdução, desenvolvimento, atividade prática, fechamento).
    4.  **Recursos Necessários:** Liste os materiais que o professor precisará.
    5.  **Forma de Avaliação:** Sugira como o professor pode avaliar o entendimento dos alunos sobre o tema.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Em caso de erro na API da IA, retornamos uma mensagem amigável
        print(f"Erro ao chamar a API do Gemini: {e}")
        return "Ocorreu um erro ao gerar o plano de aula com a IA. Tente novamente mais tarde."

def gerar_beamer_com_ia(plano_de_aula_markdown: str) -> str:
    """
    Usa a IA para converter um plano de aula em Markdown para código LaTeX Beamer.
    """
    prompt = f"""
    Atue como um especialista em LaTeX e apresentações Beamer.
    Sua tarefa é converter o plano de aula a seguir, que está em formato Markdown, para um código LaTeX Beamer completo e compilável.

    Requisitos do Código Beamer:
    1.  Use o `\\documentclass{{beamer}}`.
    2.  Use um tema visualmente agradável, como `\\usetheme{{Madrid}}` ou `\\usetheme{{Boadilla}}`.
    3.  Extraia o Título, Disciplina e Série do plano para preencher o `\\title{{}}`, `\\author{{}}` e `\\institute{{}}` da apresentação. O autor pode ser "MestraPro AI".
    4.  Crie um slide de título com `\\frame{{\\titlepage}}`.
    5.  Para cada seção principal do plano de aula (como "Objetivos de Aprendizagem", "Conteúdo Programático", etc.), crie um frame separado com `\\begin{{frame}}{{Título da Seção}}`.
    6.  Dentro de cada frame, use `\\begin{{itemize}}` e `\\item` para listar os pontos.
    7.  O código gerado deve ser exclusivamente o código LaTeX. Não inclua explicações, comentários ou a palavra "markdown".

    Aqui está o plano de aula em Markdown para ser convertido:
    ---
    {plano_de_aula_markdown}
    ---
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini para gerar Beamer: {e}")
        return "\\documentclass{{beamer}}\n\\begin{{document}}\n\\frame{{\n  \\frametitle{{Erro}}\n  Ocorreu um erro ao gerar os slides. Tente novamente.\n}}\n\\end{{document}}"