import subprocess


def query_ollama(prompt: str):
    command = ["ollama", "run", "phi3", prompt]
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()


def pharma_agent(query: str):
    prompt = f"""
You are a pharmaceutical research assistant.
Analyze the following query related to drug repurposing or respiratory health.

Query: {query}

Return a concise summary with:
1. Key molecule(s) of interest
2. Mechanism or therapeutic area
3. Summary of recent studies or clinical data
4. Potential opportunities or risks
"""
    response = query_ollama(prompt)
    return {"summary": response}
