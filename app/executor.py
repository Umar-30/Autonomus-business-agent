import json
import cohere
from app.config import COHERE_API_KEY
from app.tools.web_search import web_search
from app.tools.email_tool import send_email
from app.state import AgentState

co = cohere.Client(COHERE_API_KEY)

ROUTER_PROMPT = """
You are an expert task router. Your job is to decide which tool to use and provide the necessary arguments.
Available Tools:
1. 'web_search': For research. Requires argument 'query'.
2. 'send_email': For outreach. Requires 'to', 'subject', and 'body'.
3. 'none': For general tasks.

Task: {task}

Return ONLY a JSON object: {{"tool": "tool_name", "args": {{"arg1": "val1", ...}}}}
"""

def executor_node(state: AgentState):
    if not state["pending_tasks"]:
        return {}

    tasks = state["pending_tasks"].copy()
    current_task = tasks.pop(0)
    
    print(f"\n[NODE] Executing: {current_task}")

    # SMART ROUTING: Get JSON response from LLM
    try:
        response = co.chat(
            model="command-r-08-2024",
            message=ROUTER_PROMPT.format(task=current_task),
            response_format={ "type": "json_object" }
        )
        data = json.loads(response.text)
        tool_name = data.get("tool", "none")
        args = data.get("args", {})
    except Exception as e:
        print(f"Error parsing tool call: {e}")
        tool_name = "none"
        args = {}

    if tool_name == "web_search":
        query = args.get("query", current_task)
        result = web_search(query)
    elif tool_name == "send_email":
        result = send_email(
            to=args.get("to", "prospect@example.com"), 
            subject=args.get("subject", "Business Opportunity"), 
            body=args.get("body", f"Hi, regarding: {current_task}")
        )
    else:
        result = f"Completed manually: {current_task}"

    return {
        "pending_tasks": tasks,
        "completed_tasks": [current_task],
        "logs": [{"task": current_task, "status": "success", "output": result}]
    }
