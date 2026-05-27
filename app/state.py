from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    goal: str
    pending_tasks: List[str]
    completed_tasks: Annotated[List[str], operator.add]
    logs: Annotated[List[dict], operator.add]
