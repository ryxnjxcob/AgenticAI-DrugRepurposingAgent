from .pharma_agent import query_ollama


def business_agent(query: str):
    prompt = f"""
You are a business market analyst.
Analyze the query: "{query}"
Provide:
- Market size or trend (USD)
- Key competitors
- Growth outlook
- Strategic recommendation
"""
    response = query_ollama(prompt)
    return {"market_insights": response}
