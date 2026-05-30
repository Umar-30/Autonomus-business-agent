import streamlit as st
import time
import json
import os
from app.main import app as agent_app
from app.logger import save_to_history, HISTORY_FILE

def run_gui():
    st.set_page_config(page_title="Autonomous Business Agent", page_icon="🚀", layout="wide")

    st.title("🚀 Autonomous Business Agent")
    st.markdown("Enter your business goal and watch the AI agent plan and execute tasks for you.")

    # Sidebar: History Management
    with st.sidebar:
        st.header("📜 Run History")
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    history_data = json.load(f)
                
                if not history_data:
                    st.write("No history available.")
                else:
                    # Show last 5 runs
                    for idx, entry in enumerate(reversed(history_data[-5:])):
                        # Display by Title (Goal Name) instead of just Timestamp
                        display_name = entry.get('title', entry['timestamp'])
                        with st.expander(f"📁 {display_name}"):
                            st.caption(f"Time: {entry['timestamp']}")
                            st.write(f"**Goal:** {entry['goal']}")
                            if st.button("View Full Details", key=f"view_hist_{idx}"):
                                st.session_state.selected_report = entry['full_report']
            except Exception:
                st.write("Error loading history.")
        else:
            st.write("No history file found.")
        
        st.divider()
        st.header("🤖 About the Agent")
        st.markdown("""
        **Autonomous Business Agent** 🚀  
        An AI-powered partner that:
        - 🧠 **Plans:** Breaks goals into tasks.
        - 🔍 **Researches:** Finds leads & info.
        - ✉️ **Outreaches:** Drafts & sends emails.
        - 📊 **Summarizes:** Delivers final reports.
        
        Built with **LangGraph** & **Cohere**.
        """)

        st.divider()
        st.header("💡 Sample Goals")
        st.markdown("""
        Try these to test the agent:
        1. *\"Find 3 SEO agencies in London and draft a cold email.\"*
        2. *\"Search for top 3 AI trends in 2024 and summarize them.\"*
        """)

        st.divider()
        st.header("Agent Info")
        st.info("This agent uses LangGraph and Cohere LLM to autonomously perform business tasks.")
        if st.button("Clear File History", key="clear_history_btn"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
                st.success("History cleared!")
                time.sleep(1)
                st.rerun()

    # If a report is selected from history, show it
    if "selected_report" in st.session_state:
        st.markdown("---")
        st.markdown("### 📄 Historical Report Details")
        st.info(st.session_state.selected_report)
        if st.button("Close Report", key="close_report_btn"):
            del st.session_state.selected_report
            st.rerun()

    # Main Input
    st.markdown("---")
    goal = st.text_input("What is your business goal?", placeholder="e.g., Find 5 SaaS leads and draft outreach emails", key="goal_input")

    if st.button("Run Agent", type="primary", key="run_agent_btn") and goal:
        state = {
            "goal": goal,
            "pending_tasks": [],
            "completed_tasks": [],
            "logs": []
        }

        try:
            with st.status("🤖 Agent is working...", expanded=True) as status:
                st.write("--- 🧠 Planning phase...")
                final_state = agent_app.invoke(state)
                
                for log in final_state['logs']:
                    if log['task'] == "Planning":
                        st.success(f"✅ {log['output']}")
                    elif log['task'] == "Final Report":
                        pass 
                    else:
                        st.write(f"⚙️ **Executing:** {log['task']}")

                # SAVE TO HISTORY FILE
                save_to_history(final_state)
                status.update(label="✅ Task Complete & Saved!", state="complete", expanded=False)

            # Final Report Display
            final_answer = final_state['logs'][-1]['output']
            st.markdown("---")
            st.markdown("### ✨ Final Report")
            st.markdown(final_answer)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_gui()
