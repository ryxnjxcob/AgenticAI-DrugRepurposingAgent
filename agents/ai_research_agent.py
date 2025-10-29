from .pharma_agent import query_ollama


def ai_research_agent(query: str):
    prompt = f"""
You are an AI researcher.
Based on the topic "{query}", list:
1. AI techniques or models relevant to this field
2. Example research papers or datasets
3. How AI could accelerate discovery or analysis here
"""
    response = query_ollama(prompt)
    return {"ai_research_summary": response}
