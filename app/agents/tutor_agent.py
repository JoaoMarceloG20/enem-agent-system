

import os
import sys
from agno.agent import Agent
from agno.messages import Message
from agno.utils.logger import logger
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

class TutorAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.qdrant_client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        genai.configure(api_key=settings.gemini_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
        self.collection_name = "enem_content"

    async def handle_message(self, message: Message):
        logger.info(f"TutorAgent received message: {message.intent}")

        if message.intent == "query_subject":
            user_query = message.payload.get("text")
            if not user_query:
                logger.warning("Received query_subject intent without 'text' in payload.")
                return

            logger.info(f"Processing query: {user_query}")

            # 1. Generate embedding for the query
            query_embedding = self.embedding_model.encode(user_query).tolist()

            # 2. Search Qdrant for relevant context
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=3  # Retrieve top 3 relevant chunks
            )

            context = ""
            if search_result:
                context = "\n\n".join([hit.payload["text"] for hit in search_result])
                logger.info(f"Found {len(search_result)} relevant context chunks.")
            else:
                logger.info("No relevant context found in Qdrant.")

            # 3. Construct prompt for LLM
            prompt = f"""Você é um tutor inteligente e prestativo para alunos que estão se preparando para o ENEM. 
            Sua tarefa é responder às perguntas dos alunos de forma clara, concisa e didática, utilizando o contexto fornecido. 
            Se a pergunta não puder ser respondida com o contexto fornecido, diga que não tem informações suficientes.

            Contexto:
            {context}

            Pergunta do Aluno: {user_query}

            Resposta:"""
            
            # 4. Generate response using Gemini
            try:
                response = self.gemini_model.generate_content(prompt)
                answer = response.text
                logger.info(f"Generated answer: {answer[:100]}...")
            except Exception as e:
                logger.error(f"Error generating content with Gemini: {e}")
                answer = "Desculpe, não consegui gerar uma resposta no momento. Por favor, tente novamente mais tarde."

            # 5. Send response back
            await self.send_message(
                receiver=message.sender,
                intent="answer_query",
                payload={
                    "answer": answer,
                    "original_query": user_query,
                    "original_sender": message.sender, # Pass original sender
                    "response_channel": message.payload.get("response_channel") # Pass response channel
                }
            )
        else:
            logger.warning(f"TutorAgent received unhandled intent: {message.intent}")


