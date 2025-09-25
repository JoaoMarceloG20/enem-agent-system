#!/usr/bin/env python3
"""
Teste básico do QuizContentParser para validar a funcionalidade implementada.
"""

from app.utils.quiz_parser import parse_quiz_content, QuizParsingError
from app.api.models import SubjectEnum, DifficultyEnum

# Teste com conteúdo simples formato ENEM
test_content = """
## Questão 1

**Contexto:** A Revolução Industrial transformou profundamente as estruturas sociais e econômicas dos países europeus no século XVIII e XIX.

**Comando:** Qual dos conceitos abaixo, formulado por Karl Marx, é fundamental para compreender a estratificação social no período pós-revolução industrial?

A) Anomia
B) Fato Social
C) Ação Social
D) Luta de Classes
E) Burocracia

**Gabarito:** D
**Explicação:** Karl Marx identificou a luta de classes como o motor da história e elemento central para compreender a estratificação social no capitalismo industrial.
**Tópico:** Teoria Sociológica (Karl Marx), Estratificação Social
**Dificuldade:** medio

## Questão 2

**Contexto:** O sistema eleitoral brasileiro utiliza diferentes métodos para escolha de representantes nos três níveis de governo.

**Comando:** No sistema proporcional brasileiro, o que determina quantas vagas cada partido político conquista?

A) O número total de votos do partido mais votado
B) O quociente eleitoral e a distribuição das sobras
C) A média aritmética dos votos de todos os candidatos
D) O voto majoritário simples
E) A preferência declarada pelos eleitores

**Gabarito:** B
**Explicação:** No sistema proporcional, as vagas são distribuídas com base no quociente eleitoral (votos válidos divididos por vagas) e posteriormente as sobras são distribuídas.
**Tópico:** Sistema Eleitoral Brasileiro
**Dificuldade:** medio
"""

def test_quiz_parser():
    """Teste básico do parser de quiz"""
    print("🧪 Testando QuizContentParser...")

    try:
        # Parse do conteúdo
        questions = parse_quiz_content(
            content=test_content,
            expected_questions=2,
            default_subject=SubjectEnum.SOCIOLOGIA,
            default_difficulty=DifficultyEnum.MEDIO
        )

        print(f"✅ Parser funcionou! {len(questions)} questões extraídas.")

        # Validar primeira questão
        q1 = questions[0]
        print(f"\n📝 Questão 1:")
        print(f"   ID: {q1.question_id}")
        print(f"   Contexto: {q1.context[:50]}...")
        print(f"   Comando: {q1.command[:50]}...")
        print(f"   Alternativas: {len(q1.alternatives)} opções")
        print(f"   Gabarito: {q1.correct_answer}")
        print(f"   Tópico: {q1.topic}")
        print(f"   Matéria: {q1.subject}")
        print(f"   Dificuldade: {q1.difficulty}")

        # Validar segunda questão
        q2 = questions[1]
        print(f"\n📝 Questão 2:")
        print(f"   ID: {q2.question_id}")
        print(f"   Contexto: {q2.context[:50]}...")
        print(f"   Comando: {q2.command[:50]}...")
        print(f"   Alternativas: {len(q2.alternatives)} opções")
        print(f"   Gabarito: {q2.correct_answer}")
        print(f"   Tópico: {q2.topic}")
        print(f"   Matéria: {q2.subject}")
        print(f"   Dificuldade: {q2.difficulty}")

        # Testar geração automática de content
        from app.api.models import QuizResponse, AgentRunMetadata

        metadata = AgentRunMetadata(
            agent_id="quiz",
            agent_name="Test Quiz Agent",
            model_used="test",
            temperature=0.4,
            max_tokens=1000
        )

        response = QuizResponse(
            message="Teste de geração automática de content",
            content="",  # Será gerado automaticamente
            metadata=metadata,
            session_id="test-session",
            questions=questions
        )

        print(f"\n📄 Content gerado automaticamente:")
        print(f"   Tamanho: {len(response.content)} caracteres")
        print(f"   Primeiras linhas:")
        for line in response.content.split('\n')[:5]:
            if line.strip():
                print(f"     {line}")

        print("\n✅ Teste concluído com sucesso!")
        return True

    except QuizParsingError as e:
        print(f"❌ Erro de parsing: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    test_quiz_parser()
