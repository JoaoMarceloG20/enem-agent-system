

import sys
import os
import json
from agno.agent import Agent
from agno.messages import Message
from agno.utils.logger import logger
import google.generativeai as genai
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings
from app.db.database import SessionLocal # For database interaction
from app.db.models import User, StudyPlan, UserProgress

class StudyPlanAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        genai.configure(api_key=settings.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')

    async def handle_message(self, message: Message):
        logger.info(f"StudyPlanAgent received message: {message.intent}")

        if message.intent == "generate_study_plan":
            user_id = message.payload.get("user_id")
            duration_days = message.payload.get("duration_days", 30) # Default to 30 days
            focus_subjects = message.payload.get("focus_subjects", "geral")
            response_channel = message.payload.get("response_channel")

            if not user_id or not response_channel:
                logger.error("Missing user_id or response_channel in generate_study_plan message.")
                return

            logger.info(f"Generating study plan for user {user_id} for {duration_days} days, focusing on {focus_subjects}.")

            # 1. Retrieve user progress (simulated for now, as DB is not active)
            user_progress_data = "Nenhum histórico de progresso disponível." # Default
            # try:
            #     db = SessionLocal()
            #     user = db.query(User).filter(User.username == user_id).first() # Assuming username is user_id for simplicity
            #     if user:
            #         progress_records = db.query(UserProgress).filter(UserProgress.user_id == user.id).all()
            #         if progress_records:
            #             user_progress_data = "Histórico de progresso:\n" + "\n".join([
            #                 f"- {p.subject}: Score {p.score}, Dificuldade {p.difficulty_level} ({p.timestamp.strftime('%Y-%m-%d')})"
            #                 for p in progress_records
            #             ])
            #     db.close()
            # except Exception as e:
            #     logger.error(f"Error retrieving user progress: {e}")

            # 2. Construct prompt for LLM
            prompt = f"""Você é um assistente especializado em criar planos de estudo personalizados para o ENEM. 
            Crie um plano de estudos detalhado para um aluno se preparar para o ENEM. 
            O plano deve ter duração de {duration_days} dias e focar em {focus_subjects}. 
            Considere o seguinte histórico de progresso do aluno (se disponível):\n{user_progress_data}

            O plano deve ser estruturado dia a dia, com matérias, tópicos e sugestões de atividades (ex: ler, resolver exercícios, assistir aulas). 
            Formate a saída como um JSON, com uma chave 'plan' que é uma lista de objetos, onde cada objeto representa um dia e contém 'date', 'day_of_week', 'subjects' (lista de objetos com 'name' e 'topics'), e 'activities' (lista de strings).
            Exemplo de formato:
            {{
                "plan": [
                    {{
                        "date": "YYYY-MM-DD",
                        "day_of_week": "Segunda-feira",
                        "subjects": [
                            {{"name": "Matemática", "topics": ["Funções", "Geometria Básica"]}},
                            {{"name": "Português", "topics": ["Interpretação de Texto"]}}
                        ],
                        "activities": ["Resolver 10 exercícios de funções", "Ler artigo sobre interpretação de texto"]
                    }}
                ]
            }}
            Gere o plano completo em JSON.
            """
            
            # 3. Generate response using Gemini
            try:
                response = self.gemini_model.generate_content(prompt)
                plan_json_str = response.text.strip()
                # Attempt to parse JSON, sometimes LLMs add extra text
                if plan_json_str.startswith("```json") and plan_json_str.endswith("```"):
                    plan_json_str = plan_json_str[7:-3].strip()
                
                plan_data = json.loads(plan_json_str)
                logger.info("Study plan generated successfully.")

                # 4. Save study plan to DB (commented out for now)
                # try:
                #     db = SessionLocal()
                #     user = db.query(User).filter(User.username == user_id).first()
                #     if not user:
                #         user = User(username=user_id, email=f"{user_id}@example.com") # Create dummy user if not exists
                #         db.add(user)
                #         db.commit()
                #         db.refresh(user)
                #     
                #     new_plan = StudyPlan(
                #         user_id=user.id,
                #         start_date=datetime.utcnow(),
                #         end_date=datetime.utcnow() + timedelta(days=duration_days),
                #         goals=f"Plano de {duration_days} dias com foco em {focus_subjects}",
                #         plan_details=plan_data
                #     )
                #     db.add(new_plan)
                #     db.commit()
                #     db.refresh(new_plan)
                #     logger.info(f"Study plan saved to DB for user {user_id}.")
                # except Exception as e:
                #     logger.error(f"Error saving study plan to DB: {e}")

                # 5. Send response back to Orchestrator
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="study_plan_generated",
                    payload={
                        "status": "success",
                        "plan": plan_data,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )
                logger.info(f"Sent study plan generated message to Orchestrator for user {user_id}")

            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from Gemini response: {e}\nResponse: {plan_json_str[:500]}...")
                error_message = "Desculpe, não consegui gerar um plano de estudos válido. Por favor, tente novamente."
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="study_plan_generated",
                    payload={
                        "status": "error",
                        "message": error_message,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )
            except Exception as e:
                logger.error(f"Error generating study plan with Gemini: {e}")
                error_message = "Desculpe, não consegui gerar um plano de estudos no momento. Por favor, tente novamente mais tarde."
                await self.send_message(
                    receiver="agent_orchestrator",
                    intent="study_plan_generated",
                    payload={
                        "status": "error",
                        "message": error_message,
                        "original_sender": message.sender,
                        "response_channel": response_channel
                    }
                )

        else:
            logger.warning(f"StudyPlanAgent received unhandled intent: {message.intent}")

