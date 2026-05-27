import cohere
from app.config import COHERE_API_KEY
from app.state import AgentState

co = cohere.Client(COHERE_API_KEY)

PLANNER_PROMPT = """
You are an autonomous business planning agent.
Break the business goal into a concise list of ACTIONABLE tasks.
Each task should be a single line.
Focus on tasks that can be done via 'search' or 'email'.

Goal: {goal}

Return ONLY the list of tasks, one per line. No introduction or numbering.
"""

def planner_node(state: AgentState):
    print(f"[NODE] Planning for goal: {state['goal']}")
    
    response = co.chat(
        model="command-r-08-2024",
        message=PLANNER_PROMPT.format(goal=state['goal'])
    )

    tasks = [t.strip("- ").strip() for t in response.text.strip().split("\n") if t.strip()]
    
    return {
        "pending_tasks": tasks,
        "logs": [{"task": "Planning", "status": "success", "output": f"Generated {len(tasks)} tasks"}]
    }

def summarizer_node(state: AgentState):
    print(f"[NODE] Generating Final Report...")
    
    # Collect all logs into a single string
    context = ""
    for log in state["logs"]:
        context += f"Task: {log['task']}\nResult: {log['output']}\n\n"

    SUMMARIZER_PROMPT = f"""
    You are an AI Business Consultant. Based on the following execution logs for the goal '{state['goal']}', 
    provide a comprehensive final summary and answer to the user.
    
    Highlight:
    1. Key findings from research.
    2. Actions taken (like emails sent).
    3. Next recommended steps.

    Logs:
    {context}
    """

    response = co.chat(
        model="command-r-08-2024",
        message=SUMMARIZER_PROMPT
    )

    return {
        "logs": [{"task": "Final Report", "status": "success", "output": response.text}]
    }
