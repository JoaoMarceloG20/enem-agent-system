
import sys
import os
import json
from agno.agent import Agent
from agno.messages import Message
from agno.utils.logger import logger
import google.generativeai as genai

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
# from app.db.database import SessionLocal # Uncomment when DB is active
# from app.db.models import Question # Uncomment when DB is active

class QuizAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        genai.configure(api_key=settings.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    async def handle_message(self, message: Message):
        logger.info(f"QuizAgent received message: {message.intent}")

        if message.intent == "request_quiz_question":
            user_id = message.payload.get("user_id")
            subject = message.payload.get("subject", "geral")
            response_channel = message.payload.get("response_channel")

            if not user_id or not response_channel:
                logger.error("Missing user_id or response_channel in request_quiz_question message.")
                return

            logger.info(f"Requesting quiz question for user {user_id} on subject {subject}.")

            # Simulate fetching a question (replace with DB query later)
            question_data = {
                "question_id": "simulated_q_1",
                "text": "Qual o principal motivo da Queda da Bastilha, evento que marcou o início da Revolução Francesa?",
                "options": {
                    "A": "A insatisfação popular com a monarquia absolutista e a crise econômica.",
                    "B": "A invasão de Paris por tropas estrangeiras.",
                    "C": "A fuga do Rei Luís XVI para a Áustria.",
                    "D": "A ascensão de Napoleão Bonaparte ao poder."
                },
                "correct_answer": "A",
                "explanation": "A Queda da Bastilha simbolizou o início da Revolução Francesa, impulsionada pela insatisfação do povo com o regime absolutista e a grave crise financeira que a França enfrentava."
            }

            # Send the question to the user
            await self.send_message(
                receiver="agent_orchestrator",
                intent="quiz_question_provided",
                payload={
                    "status": "success",
                    "question": question_data,
                    "original_sender": message.sender,
                    "response_channel": response_channel
                }
            )
            logger.info(f"Provided quiz question to Orchestrator for user {user_id}")

        elif message.intent == "submit_quiz_answer":
            user_id = message.payload.get("user_id")
            question_id = message.payload.get("question_id")
            user_answer = message.payload.get("user_answer")
            response_channel = message.payload.get("response_channel")

            if not user_id or not question_id or not user_answer or not response_channel:
                logger.error("Missing required fields in submit_quiz_answer message.")
                return

            logger.info(f"User {user_id} submitted answer {user_answer} for question {question_id}.")

            # Simulate answer validation (replace with DB query and validation later)
            is_correct = (user_answer == "A") # Based on simulated question above
            feedback = "Correto!" if is_correct else "Incorreto. A resposta correta é A."

            await self.send_message(
                receiver="agent_orchestrator",
                intent="quiz_answer_feedback",
                payload={
                    "status": "success",
                    "question_id": question_id,
                    "user_answer": user_answer,
                    "is_correct": is_correct,
                    "feedback": feedback,
                    "original_sender": message.sender,
                    "response_channel": response_channel
                }
            )
            logger.info(f"Provided quiz answer feedback to Orchestrator for user {user_id}")

        else:
            logger.warning(f"QuizAgent received unhandled intent: {message.intent}")
