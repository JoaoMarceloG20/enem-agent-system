import pytest
from app.agents.tools.tutor_tools import search_educational_content, get_curriculum_guidelines
from app.agents.tools.quiz_tools import save_quiz_result, get_user_performance
from app.agents.tools.essay_grader_tools import grade_essay_competencies, save_essay_feedback
from app.agents.tools.study_plan_tools import generate_calendar_schedule, save_study_plan

class TestTools:
    def test_tutor_tools(self):
        content = search_educational_content("Bhaskara", "matematica")
        assert "Conteúdo encontrado" in content
        
        guidelines = get_curriculum_guidelines("matematica")
        assert "Competência" in guidelines

    def test_quiz_tools(self):
        result = save_quiz_result("user1", 85.0, "algebra", "medio")
        assert "sucesso" in result
        
        perf = get_user_performance("user1")
        assert "Performance" in perf

    def test_essay_tools(self):
        grades = grade_essay_competencies("texto")
        assert "competencia_1" in grades
        assert grades["total"] == 0
        
        feedback = save_essay_feedback("user1", "texto", grades, "Bom")
        assert "sucesso" in feedback

    def test_study_plan_tools(self):
        schedule = generate_calendar_schedule(20, ["matematica", "fisica"])
        assert "Segunda" in schedule
        assert schedule["Segunda"]["hours"] > 0
        
        save_msg = save_study_plan("user1", schedule)
        assert "sucesso" in save_msg
