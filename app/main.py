from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from datetime import datetime
import asyncio
import json

from agno.core import Agno
from agno.messages import Message
from agno.utils.logger import logger

from app.agents.orchestrator_agent import OrchestratorAgent
from app.agents.tutor_agent import TutorAgent
from app.agents.study_plan_agent import StudyPlanAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.essay_grader_agent import EssayGraderAgent # New import
from app.db.database import redis_client # Import our Redis client

app = FastAPI(
    title="ENEM Agent System API",
    description="API Gateway for the ENEM agentic study system.",
    version="0.1.0"
)

# Global Agno instance
agno_instance: Agno = None

class UserQuery(BaseModel):
    user_id: str
    conversation_id: str
    text: str

class StudyPlanRequest(BaseModel):
    user_id: str
    conversation_id: str
    duration_days: int = 30
    focus_subjects: str = "geral"

class QuizQuestionRequest(BaseModel):
    user_id: str
    conversation_id: str
    subject: str = "geral"

class QuizAnswerSubmission(BaseModel):
    user_id: str
    conversation_id: str
    question_id: str
    user_answer: str

class EssayGradingRequest(BaseModel):
    user_id: str
    conversation_id: str
    essay_text: str

@app.on_event("startup")
async def startup_event():
    global agno_instance
    logger.info("Initializing Agno framework and agents...")
    agno_instance = Agno()

    # Register agents
    orchestrator = OrchestratorAgent("agent_orchestrator")
    tutor = TutorAgent("tutor_agent")
    study_plan_agent = StudyPlanAgent("study_plan_agent")
    quiz_agent = QuizAgent("quiz_agent")
    essay_grader_agent = EssayGraderAgent("essay_grader_agent") # Register new agent

    agno_instance.register_agent(orchestrator)
    agno_instance.register_agent(tutor)
    agno_instance.register_agent(study_plan_agent)
    agno_instance.register_agent(quiz_agent)
    agno_instance.register_agent(essay_grader_agent) # Register new agent

    # Start Agno in a background task
    asyncio.create_task(agno_instance.run())
    logger.info("Agno framework and agents initialized.")

@app.on_event("shutdown")
async def shutdown_event():
    if agno_instance:
        logger.info("Shutting down Agno framework...")
        await agno_instance.stop()
        logger.info("Agno framework shut down.")

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.post("/api/v1/chat", tags=["Chat"])
async def chat_endpoint(query: UserQuery):
    # Define a unique channel for this conversation to receive responses
    response_channel = f"response:{query.conversation_id}"

    # 1. Convert HTTP request to MCP Message
    mcp_message = Message(
        sender=f"user_{query.user_id}",
        receiver="agent_orchestrator", # Target the main orchestrator
        intent="query_subject",
        payload={"text": query.text, "conversation_id": query.conversation_id, "response_channel": response_channel}
    )

    if not agno_instance:
        raise HTTPException(status_code=503, detail="Agent system not initialized.")

    # 2. Send MCP message to the Agno ecosystem
    await agno_instance.send_message(mcp_message)
    logger.info(f"Sent message to orchestrator for conversation {query.conversation_id}")

    # 3. Wait for a response from the agent ecosystem via Redis Pub/Sub
    pubsub = redis_client.pubsub()
    pubsub.subscribe(response_channel)

    timeout = 60 # seconds
    start_time = asyncio.get_event_loop().time()

    response_data = None
    while asyncio.get_event_loop().time() - start_time < timeout:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            response_data = json.loads(message["data"].decode('utf-8'))
            logger.info(f"Received response from Redis for conversation {query.conversation_id}")
            break
        await asyncio.sleep(0.1) # Small delay to prevent busy-waiting

    pubsub.unsubscribe(response_channel)

    if response_data:
        return {"status": "success", "response": response_data}
    else:
        logger.error(f"Timeout waiting for response for conversation {query.conversation_id}")
        raise HTTPException(status_code=504, detail="Agent response timed out.")

@app.post("/api/v1/study_plan", tags=["Study Plan"])
async def generate_study_plan_endpoint(request: StudyPlanRequest):
    response_channel = f"response:{request.conversation_id}"

    mcp_message = Message(
        sender=f"user_{request.user_id}",
        receiver="agent_orchestrator",
        intent="generate_study_plan",
        payload={
            "user_id": request.user_id,
            "duration_days": request.duration_days,
            "focus_subjects": request.focus_subjects,
            "conversation_id": request.conversation_id,
            "response_channel": response_channel
        }
    )

    if not agno_instance:
        raise HTTPException(status_code=503, detail="Agent system not initialized.")

    await agno_instance.send_message(mcp_message)
    logger.info(f"Sent study plan request to orchestrator for conversation {request.conversation_id}")

    pubsub = redis_client.pubsub()
    pubsub.subscribe(response_channel)

    timeout = 120 # Study plan generation might take longer
    start_time = asyncio.get_event_loop().time()

    response_data = None
    while asyncio.get_event_loop().time() - start_time < timeout:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            response_data = json.loads(message["data"].decode('utf-8'))
            logger.info(f"Received response from Redis for study plan conversation {request.conversation_id}")
            break
        await asyncio.sleep(0.1)

    pubsub.unsubscribe(response_channel)

    if response_data:
        return {"status": "success", "response": response_data}
    else:
        logger.error(f"Timeout waiting for study plan response for conversation {request.conversation_id}")
        raise HTTPException(status_code=504, detail="Agent response timed out.")

@app.post("/api/v1/quiz/request_question", tags=["Quiz"])
async def request_quiz_question_endpoint(request: QuizQuestionRequest):
    response_channel = f"response:{request.conversation_id}"

    mcp_message = Message(
        sender=f"user_{request.user_id}",
        receiver="agent_orchestrator",
        intent="request_quiz_question",
        payload={
            "user_id": request.user_id,
            "subject": request.subject,
            "conversation_id": request.conversation_id,
            "response_channel": response_channel
        }
    )

    if not agno_instance:
        raise HTTPException(status_code=503, detail="Agent system not initialized.")

    await agno_instance.send_message(mcp_message)
    logger.info(f"Sent quiz question request to orchestrator for conversation {request.conversation_id}")

    pubsub = redis_client.pubsub()
    pubsub.subscribe(response_channel)

    timeout = 60
    start_time = asyncio.get_event_loop().time()

    response_data = None
    while asyncio.get_event_loop().time() - start_time < timeout:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            response_data = json.loads(message["data"].decode('utf-8'))
            logger.info(f"Received response from Redis for quiz question conversation {request.conversation_id}")
            break
        await asyncio.sleep(0.1)

    pubsub.unsubscribe(response_channel)

    if response_data:
        return {"status": "success", "response": response_data}
    else:
        logger.error(f"Timeout waiting for quiz question response for conversation {request.conversation_id}")
        raise HTTPException(status_code=504, detail="Agent response timed out.")

@app.post("/api/v1/quiz/submit_answer", tags=["Quiz"])
async def submit_quiz_answer_endpoint(request: QuizAnswerSubmission):
    response_channel = f"response:{request.conversation_id}"

    mcp_message = Message(
        sender=f"user_{request.user_id}",
        receiver="agent_orchestrator",
        intent="submit_quiz_answer",
        payload={
            "user_id": request.user_id,
            "question_id": request.question_id,
            "user_answer": request.user_answer,
            "conversation_id": request.conversation_id,
            "response_channel": response_channel
        }
    )

    if not agno_instance:
        raise HTTPException(status_code=503, detail="Agent system not initialized.")

    await agno_instance.send_message(mcp_message)
    logger.info(f"Sent quiz answer submission to orchestrator for conversation {request.conversation_id}")

    pubsub = redis_client.pubsub()
    pubsub.subscribe(response_channel)

    timeout = 60
    start_time = asyncio.get_event_loop().time()

    response_data = None
    while asyncio.get_event_loop().time() - start_time < timeout:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            response_data = json.loads(message["data"].decode('utf-8'))
            logger.info(f"Received response from Redis for quiz answer submission {request.conversation_id}")
            break
        await asyncio.sleep(0.1)

    pubsub.unsubscribe(response_channel)

    if response_data:
        return {"status": "success", "response": response_data}
    else:
        logger.error(f"Timeout waiting for quiz answer submission response for conversation {request.conversation_id}")
        raise HTTPException(status_code=504, detail="Agent response timed out.")

@app.post("/api/v1/essay/grade", tags=["Essay Grading"])
async def grade_essay_endpoint(request: EssayGradingRequest):
    response_channel = f"response:{request.conversation_id}"

    mcp_message = Message(
        sender=f"user_{request.user_id}",
        receiver="agent_orchestrator",
        intent="grade_essay",
        payload={
            "user_id": request.user_id,
            "essay_text": request.essay_text,
            "conversation_id": request.conversation_id,
            "response_channel": response_channel
        }
    )

    if not agno_instance:
        raise HTTPException(status_code=503, detail="Agent system not initialized.")

    await agno_instance.send_message(mcp_message)
    logger.info(f"Sent essay grading request to orchestrator for conversation {request.conversation_id}")

    pubsub = redis_client.pubsub()
    pubsub.subscribe(response_channel)

    timeout = 180 # Essay grading might take longer
    start_time = asyncio.get_event_loop().time()

    response_data = None
    while asyncio.get_event_loop().time() - start_time < timeout:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message:
            response_data = json.loads(message["data"].decode('utf-8'))
            logger.info(f"Received response from Redis for essay grading {request.conversation_id}")
            break
        await asyncio.sleep(0.1)

    pubsub.unsubscribe(response_channel)

    if response_data:
        return {"status": "success", "response": response_data}
    else:
        logger.error(f"Timeout waiting for essay grading response for conversation {request.conversation_id}")
        raise HTTPException(status_code=504, detail="Agent response timed out.")