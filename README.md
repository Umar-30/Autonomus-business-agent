# 🚀 Autonomous Business Agent

An AI-powered agent built with **LangGraph** and **Cohere** that autonomously plans and executes business goals. From market research to lead generation and outreach, this agent handles the workflow for you.

## ✨ Features

-   **Autonomous Planning:** Automatically breaks down complex goals into actionable tasks.
-   **Smart Routing:** Decides which tool (Search, Email, or LLM) is best for each task.
-   **Web Research:** Uses Tavily to search the web for up-to-date information.
-   **Email Outreach:** Drafts and sends emails as part of the execution flow.
-   **Run History:** Keeps track of previous goals and reports in the Streamlit UI.
-   **Dual Interface:** Run it from the terminal or through a sleek web interface.

## 🛠️ Tech Stack

-   **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph)
-   **LLM:** [Cohere Command R](https://cohere.com/)
-   **Web UI:** [Streamlit](https://streamlit.io/)
-   **Search:** [Tavily](https://tavily.com/)
-   **Environment:** Python 3.14+

## 🚀 Getting Started

### Prerequisites

-   Python 3.14+
-   API keys for **Cohere** and **Tavily**.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/autonomous-business-agent.git
    cd autonomous-business-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the root directory:
    ```env
    COHERE_API_KEY=your_cohere_key
    TAVILY_API_KEY=your_tavily_key
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_app_password
    ```

### Running the Agent

#### Web Interface (Recommended)
```bash
streamlit run ui.py
```

#### Command Line
```bash
python -m app.main
```

## 🏗️ Architecture

The agent follows a circular graph workflow:
1.  **Start** ➔ **Planner** (Creates task list)
2.  **Planner** ➔ **Executor** (Processes the first task)
3.  **Executor** ➔ **Decision** (Are there more tasks?)
    -   If **Yes** ➔ Back to **Executor**
    -   If **No** ➔ **Summarizer**
4.  **Summarizer** ➔ **End** (Final Report)

## 📁 Project Structure

```text
├── app/
│   ├── tools/          # External tool implementations
│   ├── executor.py     # Task execution logic
│   ├── planner.py      # Planning & Summarization nodes
│   ├── main.py         # Graph definition & CLI entry
│   └── state.py        # Shared agent state
├── logs/               # Run history and logs
├── ui.py               # Streamlit web interface
├── requirements.txt    # Dependencies
└── .env.example        # Template for secrets
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
