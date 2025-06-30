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