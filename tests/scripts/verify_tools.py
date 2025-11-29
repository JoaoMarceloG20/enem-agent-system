"""
Verify Agent Tools

Script to verify if agents can successfully load their tools.
"""
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from app.agents.tutor_agent import TutorAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.essay_grader_agent import EssayGraderAgent
from app.agents.study_plan_agent import StudyPlanAgent

def verify_tools():
    agents = [
        ("TutorAgent", TutorAgent()),
        ("QuizAgent", QuizAgent()),
        ("EssayGraderAgent", EssayGraderAgent()),
        ("StudyPlanAgent", StudyPlanAgent())
    ]
    
    all_passed = True
    
    print("Verifying Agent Tools...")
    print("-" * 30)
    
    for name, agent in agents:
        tools = agent.get_agent_tools()
        tool_count = len(tools)
        status = "PASS" if tool_count > 0 else "FAIL"
        
        if status == "FAIL":
            all_passed = False
            
        print(f"{name}: {tool_count} tools loaded -> {status}")
        
    print("-" * 30)
    if all_passed:
        print("All agents loaded tools successfully!")
        sys.exit(0)
    else:
        print("Some agents failed to load tools.")
        sys.exit(1)

if __name__ == "__main__":
    verify_tools()
