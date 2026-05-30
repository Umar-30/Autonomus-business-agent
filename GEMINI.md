# Autonomous Business Agent Overview

This project is an AI-powered agent designed to autonomously plan and execute business goals. It leverages **LangGraph** for workflow orchestration and **Cohere** for natural language understanding and task execution.

## Core Architecture

The agent operates as a state machine using LangGraph. The workflow consists of three primary nodes:

1.  **Planner Node:** Breaks down a high-level business goal into a series of actionable tasks.
2.  **Executor Node:** Iterates through pending tasks, routing them to appropriate tools (Web Search, Email) or processing them directly using the LLM.
3.  **Summarizer Node:** Consolidates all execution results into a comprehensive final report for the user.

## Key Technologies

-   **LangGraph:** Manages the state and control flow of the agent.
-   **Cohere (Command R):** Used for planning, routing, and summarization.
-   **Streamlit:** Provides a user-friendly web interface for interacting with the agent.
-   **Tavily:** Powers the web search capabilities for research tasks.

## Project Structure

-   `app/`: Contains the core logic.
    -   `main.py`: Entry point for the CLI and LangGraph workflow definition.
    -   `planner.py`: Defines the Planning and Summarization nodes.
    -   `executor.py`: Defines the Execution node and tool routing logic.
    -   `state.py`: Defines the shared state structure for the agent.
    -   `tools/`: Implementation of external tools (Email, Web Search).
-   `ui.py`: The Streamlit web application.
-   `requirements.txt`: Project dependencies.

## Key Commands

-   **Run CLI:** `python -m app.main`
-   **Run Web UI:** `streamlit run ui.py`
