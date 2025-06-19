# Em: test_db.py

# Importa as ferramentas de banco de dados e os modelos que criamos
from app.database import SessionLocal
from app.models.schemas import LessonPlan, User

def run_db_test():
    print("Iniciando teste de banco de dados...")
    
    # Cria uma nova sessão com o banco
    db = SessionLocal()
    
    print("-> Conexão estabelecida.")

    try:
        # --- PASSO 1: Inserir um usuário e um plano de aula de teste ---
        print("\nPASSO 1: Tentando inserir dados...")
        
        # Cria um usuário de teste (necessário por causa da relação)
        usuario_teste = User(email="teste@exemplo.com", hashed_password="abc")
        db.add(usuario_teste)
        db.commit()
        db.refresh(usuario_teste)
        
        # Cria um plano de teste associado a esse usuário
        plano_teste = LessonPlan(
            topic="Tópico de Teste",
            grade="1º Ano",
            subject="Teste",
            content="Este é o conteúdo do plano de aula de teste.",
            owner_id=usuario_teste.id # Associa o plano ao usuário
        )
        
        db.add(plano_teste)
        db.commit()
        db.refresh(plano_teste) # Atualiza o objeto com o ID gerado pelo banco
        
        print(f"   => ✅ SUCESSO! Plano inserido com ID: {plano_teste.id} para o usuário ID: {usuario_teste.id}")

        # --- PASSO 2: Verificar se o plano existe ---
        print("\nPASSO 2: Buscando o plano para confirmar...")
        
        plano_encontrado = db.query(LessonPlan).filter(LessonPlan.id == plano_teste.id).first()
        
        if plano_encontrado:
            print(f"   => ✅ SUCESSO! Plano '{plano_encontrado.topic}' encontrado no banco.")
        else:
            raise Exception("FALHA! Não foi possível encontrar o plano que acabamos de inserir.")

        # --- PASSO 3: Remover os dados de teste ---
        print(f"\nPASSO 3: Tentando remover o plano ID {plano_teste.id} e o usuário ID {usuario_teste.id}...")
        
        db.delete(plano_encontrado)
        db.delete(usuario_teste)
        db.commit()
        
        print("   => ✅ SUCESSO! Dados de teste removidos.")
        print("\nTeste do banco de dados concluído com sucesso!")

    except Exception as e:
        print(f"\n❌ OCORREU UM ERRO: {e}")
        db.rollback() # Desfaz qualquer alteração em caso de erro
    finally:
        print("\nFechando conexão com o banco.")
        db.close() # Sempre feche a conexão no final

# Roda a função de teste quando o script é executado
if __name__ == "__main__":
    run_db_test()