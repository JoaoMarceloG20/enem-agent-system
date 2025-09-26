"""
Quiz Content Parser

Utilities for parsing generated quiz content into structured QuizQuestion objects.
Handles various formats and ensures consistency between content and structured data.
"""

import re
import uuid
from typing import List, Dict, Any, Optional, Tuple
from app.api.models import QuizQuestion, SubjectEnum, DifficultyEnum


class QuizParsingError(Exception):
    """Custom exception for quiz parsing errors"""
    pass


class QuizContentParser:
    """
    Robust parser for converting LLM-generated quiz content into structured QuizQuestion objects.

    Supports multiple formats:
    - Standard ENEM format with context/command structure
    - Simple question format
    - Mixed formats within the same content
    """

    # Regex patterns for parsing different question components
    QUESTION_SEPARATOR = re.compile(r"(?:^|\n)\s*#{1,4}\s*Questão\s*(\d+)", re.MULTILINE | re.IGNORECASE)
    CONTEXT_PATTERN = re.compile(r"\*\*Contexto:?\*\*\s*(.*?)(?=\*\*|\n[A-E]\)|\n\n|$)", re.DOTALL | re.IGNORECASE)
    COMMAND_PATTERN = re.compile(r"\*\*(?:Comando|Pergunta):?\*\*\s*(.*?)(?=\*\*|\n[A-E]\)|\n\n|$)", re.DOTALL | re.IGNORECASE)
    QUESTION_PATTERN = re.compile(r"\*\*Questão:?\*\*\s*(.*?)(?=\*\*|\n[A-E]\)|\n\n|$)", re.DOTALL | re.IGNORECASE)

    ALTERNATIVES_PATTERN = re.compile(r"([A-E])\)\s*(.*?)(?=\n[A-E]\)|\n\*\*|\*\*|$)", re.DOTALL)
    GABARITO_PATTERN = re.compile(r"\*\*Gabarito:?\*\*\s*([A-E])", re.IGNORECASE)
    EXPLANATION_PATTERN = re.compile(r"\*\*(?:Explicação|Justificativa):?\*\*\s*(.*?)(?=\*\*|\n\n|$)", re.DOTALL | re.IGNORECASE)
    TOPIC_PATTERN = re.compile(r"\*\*Tópico:?\*\*\s*(.*?)(?=\*\*|\n\n|$)", re.DOTALL | re.IGNORECASE)
    DIFFICULTY_PATTERN = re.compile(r"\*\*Dificuldade:?\*\*\s*(facil|medio|dificil)", re.IGNORECASE)

    def __init__(self):
        self.default_subject = SubjectEnum.MATEMATICA
        self.default_difficulty = DifficultyEnum.MEDIO

    def parse_quiz_content(
        self,
        content: str,
        expected_questions: int,
        default_subject: Optional[SubjectEnum] = None,
        default_difficulty: Optional[DifficultyEnum] = None
    ) -> List[QuizQuestion]:
        """
        Parse quiz content into structured QuizQuestion objects.

        Args:
            content: Raw content from LLM
            expected_questions: Expected number of questions
            default_subject: Default subject if not specified in content
            default_difficulty: Default difficulty if not specified in content

        Returns:
            List of structured QuizQuestion objects

        Raises:
            QuizParsingError: If parsing fails or inconsistencies are found
        """
        if default_subject:
            self.default_subject = default_subject
        if default_difficulty:
            self.default_difficulty = default_difficulty

        # Clean content
        content = self._clean_content(content)

        # Split into individual questions
        question_blocks = self._split_into_questions(content)

        if len(question_blocks) != expected_questions:
            raise QuizParsingError(
                f"Expected {expected_questions} questions, found {len(question_blocks)}"
            )

        questions = []
        for i, block in enumerate(question_blocks):
            try:
                question = self._parse_single_question(block, i + 1)
                questions.append(question)
            except Exception as e:
                raise QuizParsingError(f"Error parsing question {i + 1}: {str(e)}")

        # Validate consistency
        self._validate_questions_consistency(questions)

        return questions

    def _clean_content(self, content: str) -> str:
        """Clean and normalize content"""
        # Remove excessive whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'^\s+|\s+$', '', content, flags=re.MULTILINE)

        # Normalize markdown formatting
        content = re.sub(r'\*{3,}([^*]+)\*{3,}', r'**\1**', content)

        return content.strip()

    def _split_into_questions(self, content: str) -> List[str]:
        """Split content into individual question blocks"""
        # Find question separators
        separators = list(self.QUESTION_SEPARATOR.finditer(content))

        if not separators:
            # Try alternative patterns
            # Look for numbered lists or question patterns
            alt_pattern = re.compile(r"(?:^|\n)\s*(\d+)[\.\)]\s*", re.MULTILINE)
            separators = list(alt_pattern.finditer(content))

            if not separators:
                # If no clear separators, treat as single question
                return [content]

        question_blocks = []
        for i, separator in enumerate(separators):
            start = separator.start()
            end = separators[i + 1].start() if i + 1 < len(separators) else len(content)
            block = content[start:end].strip()
            if block:
                question_blocks.append(block)

        return question_blocks

    def _parse_single_question(self, block: str, question_number: int) -> QuizQuestion:
        """Parse a single question block into QuizQuestion object"""

        # Extract components
        context = self._extract_context(block)
        command = self._extract_command(block)
        alternatives = self._extract_alternatives(block)
        correct_answer = self._extract_gabarito(block)
        explanation = self._extract_explanation(block)
        topic = self._extract_topic(block)
        difficulty = self._extract_difficulty(block)

        # Validate required fields
        if not command:
            raise QuizParsingError("Command/question text not found")

        if len(alternatives) != 5:
            raise QuizParsingError(f"Expected 5 alternatives, found {len(alternatives)}")

        if not correct_answer or correct_answer not in alternatives:
            raise QuizParsingError(f"Invalid correct answer: {correct_answer}")

        if not explanation:
            raise QuizParsingError("Explanation not found")

        return QuizQuestion(
            question_id=f"q_{question_number}",
            context=context or "Contexto da questão não especificado.",
            command=command,
            alternatives=alternatives,
            correct_answer=correct_answer,
            explanation=explanation,
            topic=topic or "Tópico geral",
            difficulty=difficulty or self.default_difficulty,
            subject=self.default_subject
        )

    def _extract_context(self, block: str) -> str:
        """Extract context from question block"""
        match = self.CONTEXT_PATTERN.search(block)
        if match:
            return match.group(1).strip()

        # Try to find context before the first alternative
        lines = block.split('\n')
        context_lines = []
        found_alternative = False

        for line in lines:
            line = line.strip()
            if re.match(r'^[A-E]\)', line):
                found_alternative = True
                break
            if line and not line.startswith('**') and not line.startswith('#'):
                context_lines.append(line)

        return ' '.join(context_lines) if context_lines else ""

    def _extract_command(self, block: str) -> str:
        """Extract command/question from block"""
        # First try explicit command pattern
        match = self.COMMAND_PATTERN.search(block)
        if match:
            return match.group(1).strip()

        # Try question pattern
        match = self.QUESTION_PATTERN.search(block)
        if match:
            return match.group(1).strip()

        # Look for **Comando:** pattern specifically
        comando_pattern = re.compile(r"\*\*Comando:?\*\*\s*(.*?)(?=\*\*|A\)|$)", re.DOTALL | re.IGNORECASE)
        match = comando_pattern.search(block)
        if match:
            return match.group(1).strip()

        # Try to find question text before alternatives
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line and line.endswith('?') and not line.startswith('**') and not line.startswith('#'):
                return line

        # Fallback: look for imperative sentences
        for line in lines:
            line = line.strip()
            if line and any(word in line.lower() for word in ['qual', 'quais', 'como', 'onde', 'quando', 'por que', 'determine', 'calcule', 'identifique']):
                return line

        # Look for lines that look like questions (contain interrogative words)
        for line in lines:
            line = line.strip()
            if (line and
                not line.startswith('**') and
                not line.startswith('#') and
                not re.match(r'^[A-E]\)', line) and
                len(line) > 10):  # Reasonable question length
                return line

        raise QuizParsingError("Could not extract command/question")

    def _extract_alternatives(self, block: str) -> Dict[str, str]:
        """Extract alternatives from block"""
        alternatives = {}
        matches = self.ALTERNATIVES_PATTERN.findall(block)

        for letter, text in matches:
            alternatives[letter] = text.strip()

        # Ensure we have A-E
        expected_letters = ['A', 'B', 'C', 'D', 'E']
        for letter in expected_letters:
            if letter not in alternatives:
                alternatives[letter] = f"Alternativa {letter} não encontrada"

        return {k: alternatives[k] for k in expected_letters}

    def _extract_gabarito(self, block: str) -> str:
        """Extract correct answer from block"""
        match = self.GABARITO_PATTERN.search(block)
        if match:
            return match.group(1).upper()

        # Try alternative patterns
        patterns = [
            re.compile(r"(?:resposta|answer|correct):\s*([A-E])", re.IGNORECASE),
            re.compile(r"([A-E])\s*(?:é|está|is)\s*(?:correta|correct)", re.IGNORECASE)
        ]

        for pattern in patterns:
            match = pattern.search(block)
            if match:
                return match.group(1).upper()

        # Default to A if not found (will trigger validation error)
        return "A"

    def _extract_explanation(self, block: str) -> str:
        """Extract explanation from block"""
        match = self.EXPLANATION_PATTERN.search(block)
        if match:
            return match.group(1).strip()

        # Try alternative patterns
        patterns = [
            re.compile(r"(?:porque|justificativa|razão):\s*(.*?)(?=\*\*|\n\n|$)", re.DOTALL | re.IGNORECASE),
            re.compile(r"(?:a resposta correta é).*?(?:porque|pois)\s*(.*?)(?=\*\*|\n\n|$)", re.DOTALL | re.IGNORECASE)
        ]

        for pattern in patterns:
            match = pattern.search(block)
            if match:
                return match.group(1).strip()

        return "Explicação não fornecida."

    def _extract_topic(self, block: str) -> str:
        """Extract topic from block"""
        match = self.TOPIC_PATTERN.search(block)
        if match:
            return match.group(1).strip()

        return "Tópico não especificado"

    def _extract_difficulty(self, block: str) -> DifficultyEnum:
        """Extract difficulty from block"""
        match = self.DIFFICULTY_PATTERN.search(block)
        if match:
            difficulty_map = {
                'facil': DifficultyEnum.FACIL,
                'medio': DifficultyEnum.MEDIO,
                'dificil': DifficultyEnum.DIFICIL
            }
            return difficulty_map.get(match.group(1).lower(), self.default_difficulty)

        return self.default_difficulty

    def _validate_questions_consistency(self, questions: List[QuizQuestion]) -> None:
        """Validate consistency across all questions"""
        if not questions:
            raise QuizParsingError("No questions parsed")

        for i, question in enumerate(questions):
            # Validate alternatives
            if len(question.alternatives) != 5:
                raise QuizParsingError(f"Question {i+1}: Invalid number of alternatives")

            expected_keys = set(['A', 'B', 'C', 'D', 'E'])
            if set(question.alternatives.keys()) != expected_keys:
                raise QuizParsingError(f"Question {i+1}: Missing or invalid alternative keys")

            # Validate correct answer
            if question.correct_answer not in question.alternatives:
                raise QuizParsingError(f"Question {i+1}: Correct answer not in alternatives")

            # Validate required fields
            required_fields = ['context', 'command', 'explanation', 'topic']
            for field in required_fields:
                if not getattr(question, field):
                    raise QuizParsingError(f"Question {i+1}: Missing {field}")


def parse_quiz_content(
    content: str,
    expected_questions: int,
    default_subject: Optional[SubjectEnum] = None,
    default_difficulty: Optional[DifficultyEnum] = None
) -> List[QuizQuestion]:
    """
    Convenience function for parsing quiz content.

    Args:
        content: Raw content from LLM
        expected_questions: Expected number of questions
        default_subject: Default subject if not specified
        default_difficulty: Default difficulty if not specified

    Returns:
        List of structured QuizQuestion objects
    """
    parser = QuizContentParser()
    return parser.parse_quiz_content(
        content=content,
        expected_questions=expected_questions,
        default_subject=default_subject,
        default_difficulty=default_difficulty
    )
