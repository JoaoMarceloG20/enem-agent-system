
import sys
import os
import json
from agno.agent import Agent
from agno.messages import Message
from agno.utils.logger import logger

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import redis_client # Import Redis client

class OrchestratorAgent(Agent):
    def __init__(self, agent_id: str):
        super().__init__(agent_id)

    async def handle_message(self, message: Message):
        logger.info(f"OrchestratorAgent received message: {message.intent} from {message.sender}")

        if message.intent == "query_subject":
            # Extract the response_channel from the payload to know where to send the final answer
            response_channel = message.payload.get("response_channel")
            if not response_channel:
                logger.error(f"No response_channel found in query_subject message from {message.sender}")
                return

            # Forward the query to the TutorAgent, preserving the response_channel
            await self.send_message(
                receiver="tutor_agent",
                intent=message.intent,
                payload=message.payload, # Payload already contains response_channel
                sender=message.sender # Preserve original sender for response routing
            )
        elif message.intent == "generate_study_plan":
            # Extract the response_channel from the payload
            response_channel = message.payload.get("response_channel")
            if not response_channel:
                logger.error(f"No response_channel found in generate_study_plan message from {message.sender}")
                return

            # Forward the request to the StudyPlanAgent
            await self.send_message(
                receiver="study_plan_agent",
                intent=message.intent,
                payload=message.payload,
                sender=message.sender
            )
        elif message.intent == "request_quiz_question":
            response_channel = message.payload.get("response_channel")
            if not response_channel:
                logger.error(f"No response_channel found in request_quiz_question message from {message.sender}")
                return
            await self.send_message(
                receiver="quiz_agent",
                intent=message.intent,
                payload=message.payload,
                sender=message.sender
            )
        elif message.intent == "submit_quiz_answer":
            response_channel = message.payload.get("response_channel")
            if not response_channel:
                logger.error(f"No response_channel found in submit_quiz_answer message from {message.sender}")
                return
            await self.send_message(
                receiver="quiz_agent",
                intent=message.intent,
                payload=message.payload,
                sender=message.sender
            )
        elif message.intent == "grade_essay":
            response_channel = message.payload.get("response_channel")
            if not response_channel:
                logger.error(f"No response_channel found in grade_essay message from {message.sender}")
                return
            await self.send_message(
                receiver="essay_grader_agent",
                intent=message.intent,
                payload=message.payload,
                sender=message.sender
            )
        elif message.intent == "answer_query":
            # This is a response from a specialist agent (e.g., TutorAgent)
            # We need to publish this answer back to the FastAPI gateway via Redis
            original_sender = message.payload.get("original_sender") # The original sender (user_id)
            response_channel = message.payload.get("response_channel") # The channel to publish to

            if not original_sender or not response_channel:
                logger.error(f"Missing original_sender or response_channel in answer_query message from {message.sender}")
                return

            answer_payload = {
                "answer": message.payload.get("answer"),
                "original_query": message.payload.get("original_query")
            }
            
            # Publish the answer to the Redis channel
            redis_client.publish(response_channel, json.dumps(answer_payload))
            logger.info(f"Published answer to Redis channel {response_channel} for original sender {original_sender}")
        elif message.intent == "study_plan_generated":
            # This is a response from the StudyPlanAgent
            original_sender = message.payload.get("original_sender")
            response_channel = message.payload.get("response_channel")

            if not original_sender or not response_channel:
                logger.error(f"Missing original_sender or response_channel in study_plan_generated message from {message.sender}")
                return
            
            plan_payload = {
                "status": message.payload.get("status"),
                "plan": message.payload.get("plan"),
                "message": message.payload.get("message")
            }

            redis_client.publish(response_channel, json.dumps(plan_payload))
            logger.info(f"Published study plan to Redis channel {response_channel} for original sender {original_sender}")
        elif message.intent == "quiz_question_provided":
            original_sender = message.payload.get("original_sender")
            response_channel = message.payload.get("response_channel")
            if not original_sender or not response_channel:
                logger.error(f"Missing original_sender or response_channel in quiz_question_provided message from {message.sender}")
                return
            quiz_payload = {
                "status": message.payload.get("status"),
                "question": message.payload.get("question")
            }
            redis_client.publish(response_channel, json.dumps(quiz_payload))
            logger.info(f"Published quiz question to Redis channel {response_channel} for original sender {original_sender}")
        elif message.intent == "quiz_answer_feedback":
            original_sender = message.payload.get("original_sender")
            response_channel = message.payload.get("response_channel")
            if not original_sender or not response_channel:
                logger.error(f"Missing original_sender or response_channel in quiz_answer_feedback message from {message.sender}")
                return
            feedback_payload = {
                "status": message.payload.get("status"),
                "question_id": message.payload.get("question_id"),
                "user_answer": message.payload.get("user_answer"),
                "is_correct": message.payload.get("is_correct"),
                "feedback": message.payload.get("feedback")
            }
            redis_client.publish(response_channel, json.dumps(feedback_payload))
            logger.info(f"Published quiz answer feedback to Redis channel {response_channel} for original sender {original_sender}")
        elif message.intent == "essay_graded":
            original_sender = message.payload.get("original_sender")
            response_channel = message.payload.get("response_channel")
            if not original_sender or not response_channel:
                logger.error(f"Missing original_sender or response_channel in essay_graded message from {message.sender}")
                return
            essay_payload = {
                "status": message.payload.get("status"),
                "grade": message.payload.get("grade"),
                "message": message.payload.get("message")
            }
            redis_client.publish(response_channel, json.dumps(essay_payload))
            logger.info(f"Published essay grade to Redis channel {response_channel} for original sender {original_sender}")
        else:
            logger.warning(f"OrchestratorAgent received unhandled intent: {message.intent}")
