
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

class EssayGraderAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        genai.configure(api_key=settings.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    async def handle_message(self, message: Message):
        logger.info(f"EssayGraderAgent received message: {message.intent}")

        if message.intent == "grade_essay":
            user_id = message.payload.get("user_id")
            essay_text = message.payload.get("essay_text")
            response_channel = message.payload.get("response_channel")

            if not user_id or not essay_text or not response_channel:
                logger.error("Missing user_id, essay_text or response_channel in grade_essay message.")
                return

            logger.info(f"Grading essay for user {user_id} (first 50 chars): {essay_text[:50]}...")

            # Construct prompt for LLM for essay grading
            prompt = f"""Você é um corretor de redações do ENEM. Sua tarefa é avaliar a redação fornecida 
            com base nas 5 competências do ENEM (Domínio da norma padrão, Compreensão da proposta, 
            Seleção e organização de argumentos, Demonstração de conhecimento dos mecanismos linguísticos, 
            Proposta de intervenção). 
            Forneça um feedback detalhado para cada competência e uma nota estimada de 0 a 1000. 
            Apresente a saída em formato JSON, com as seguintes chaves:
            - 'competencias': um objeto com chaves para cada competência (C1 a C5) e um feedback textual para cada uma.
            - 'nota_estimada': um número inteiro de 0 a 1000.
            - 'feedback_geral': um feedback textual geral sobre a redação.

            Redação a ser avaliada:
            {essay_text}

            JSON de avaliação:"""
            
            try:
                response = self.gemini_model.generate_content(prompt)
                grade_json_str = response.text.strip()
                if grade_json_str.startswith("```json") and grade_json_str.endswith("```"):
                    grade_json_str = grade_json_str[7:-3].strip()
                
                grade_data = json.loads(grade_json_str)
                logger.info("Essay graded successfully.")

                # Send response back to Orchestrator
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="essay_graded",
                    payload={
                        "status": "success",
                        "grade": grade_data,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from Gemini response: {e}\nResponse: {grade_json_str[:500]}...")
                error_message = "Desculpe, não consegui corrigir a redação. O formato da resposta do LLM não é válido."
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="essay_graded",
                    payload={
                        "status": "error",
                        "message": error_message,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )
            except Exception as e:
                logger.error(f"Error grading essay with Gemini: {e}")
                error_message = "Desculpe, não consegui corrigir a redação no momento. Por favor, tente novamente mais tarde."
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="essay_graded",
                    payload={
                        "status": "error",
                        "message": error_message,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )
        else:
            logger.warning(f"EssayGraderAgent received unhandled intent: {message.intent}")
