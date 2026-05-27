import os
from tavily import TavilyClient
from app.config import TAVILY_API_KEY

def web_search(query: str):
    """Performs a real web search using Tavily API."""
    if not TAVILY_API_KEY:
        return "Error: TAVILY_API_KEY not found in environment."

    try:
        print(f"[TOOL] Searching Tavily for: {query}")
        tavily = TavilyClient(api_key=TAVILY_API_KEY)
        response = tavily.search(query=query, search_depth="advanced")
        
        results = response.get('results', [])
        if not results:
            return f"No real-world results found for '{query}'."

        formatted_results = "\n".join([f"- {r['title']}: {r['url']}\n  {r['content'][:200]}..." for r in results[:3]])
        return f"Top search results for '{query}':\n{formatted_results}"

    except Exception as e:
        return f"Error during web search: {str(e)}"
