import json
import os
from datetime import datetime

LOGS_DIR = "logs"
HISTORY_FILE = os.path.join(LOGS_DIR, "history.json")

def save_to_history(final_state):
    """Saves the final state of an agent run to a JSON history file."""
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    # Prepare entry
    goal_text = final_state.get("goal", "No Goal")
    title = (goal_text[:30] + '...') if len(goal_text) > 30 else goal_text

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "title": title,
        "goal": goal_text,
        "tasks_completed": final_state.get("completed_tasks", []),
        "full_report": final_state["logs"][-1]["output"] if final_state["logs"] else ""
    }

    # Load existing history
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            history = []

    # Append new entry
    history.append(entry)

    # Save back to file
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    return HISTORY_FILE

def log_step(task, status, output):
    """Standard logging to console."""
    log = {
        "time": str(datetime.now()),
        "task": task,
        "status": status,
        "output": output
    }
    print(log)
    return log
