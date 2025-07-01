"""
ENEM Tutor API - Versão Simplificada
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv("../config/.env")

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# Criar app FastAPI
app = FastAPI(title="ENEM Tutor API", version="1.0.0")

# Modelos de dados
class ChatRequest(BaseModel):
    message: str

class StudyPlanRequest(BaseModel):
    duration_days: int = 30
    focus_subjects: str = "geral"

class QuizRequest(BaseModel):
    subject: str = "geral"

class EssayRequest(BaseModel):
    essay_text: str

# Endpoints
@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        prompt = f"Você é um tutor do ENEM. Responda de forma clara: {request.message}"
        response = model.generate_content(prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/study-plan")
def study_plan(request: StudyPlanRequest):
    try:
        prompt = f"""Crie um plano de estudos para o ENEM:
        - Duração: {request.duration_days} dias
        - Foco: {request.focus_subjects}
        - Estruture por semanas com matérias e tópicos"""
        
        response = model.generate_content(prompt)
        return {"plan": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/quiz")
def quiz(request: QuizRequest):
    try:
        prompt = f"""Crie uma questão do ENEM sobre {request.subject}:
        Formato: Pergunta + 5 alternativas (A-E) + resposta correta + explicação"""
        
        response = model.generate_content(prompt)
        return {"quiz": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/essay")
def essay(request: EssayRequest):
    try:
        prompt = f"""Corrija esta redação do ENEM avaliando as 5 competências:
        
        {request.essay_text}
        
        Dê nota (0-200) para cada competência e feedback detalhado."""
        
        response = model.generate_content(prompt)
        return {"grade": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)