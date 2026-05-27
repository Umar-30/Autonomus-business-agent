from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.planner import planner_node, summarizer_node
from app.executor import executor_node

def should_continue(state: AgentState):
    """Determines if there are more tasks to execute."""
    if state["pending_tasks"]:
        return "executor"
    return "summarizer"

# Initialize the graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("summarizer", summarizer_node)

# Set Entry Point
workflow.set_entry_point("planner")

# Define Edges
workflow.add_edge("planner", "executor")
workflow.add_conditional_edges("executor", should_continue)
workflow.add_edge("summarizer", END)

# Compile
app = workflow.compile()

def run_agent():
    print("\n" + "="*50)
    print("      🚀 AUTONOMOUS BUSINESS AGENT v2.1")
    print("="*50)
    
    user_goal = input("\n[?] What is your business goal today? \n> ")
    
    if not user_goal.strip():
        print("[!] Goal cannot be empty. Exiting...")
        return

    initial_state = {
        "goal": user_goal,
        "pending_tasks": [],
        "completed_tasks": [],
        "logs": []
    }

    print("\n--- 🧠 AGENT IS WORKING (Please wait...) ---")
    final_state = app.invoke(initial_state)
    
    # Get the final summary from the last log entry
    final_answer = final_state['logs'][-1]['output']

    print("\n" + "="*50)
    print("✨ AGENT'S FINAL RESPONSE")
    print("="*50)
    print(f"\n{final_answer}\n")
    print("="*50)
    print("✅ PROCESS COMPLETE")
    print(f"Goal: {final_state['goal']}")
    print(f"Total Steps: {len(final_state['logs'])}")
    print("="*50 + "\n")

if __name__ == "__main__":
    try:
        run_agent()
    except KeyboardInterrupt:
        print("\n\n[!] Agent stopped by user. Goodbye!")
