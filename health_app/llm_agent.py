import requests
import chromadb

# Replace with your free Groq API key from https://console.groq.com/
GROQ_API_KEY = "API KEYS"

def query_vector_db(user_query):
    """
    Retrieves relevant clinical/lifestyle guidelines from local ChromaDB.
    """
    try:
        client = chromadb.PersistentClient(path="./health_knowledge_db")
        collection = client.get_collection(name="lifestyle_guidelines")
        
        # Perform similarity search
        results = collection.query(query_texts=[user_query], n_results=2)
        documents = results.get("documents", [[]])[0]
        
        return " ".join(documents) if documents else "No specific guidelines found."
    except Exception as e:
        return f"Database query error: {str(e)}"

def generate_recommendation(vitals_data, user_log):
    """
    Combines biometric metrics, user context, and local RAG context to query Groq LLM.
    """
    # Step A: Get relevant guideline context via local vector store
    combined_query = f"Heart rate: {vitals_data['heart_rate_bpm']} bpm, HRV RMSSD: {vitals_data['hrv_rmssd_ms']}. User says: {user_log}"
    context = query_vector_db(combined_query)
    
    # Step B: Build system prompt with guardrails
    prompt = f"""
    You are an intelligent, supportive lifestyle health assistant.
    You DO NOT provide medical diagnoses or prescribe medical treatment.

    Clinical Guideline Context:
    {context}

    Current User Biometrics:
    - Heart Rate: {vitals_data['heart_rate_bpm']} BPM
    - HRV RMSSD: {vitals_data['hrv_rmssd_ms']} ms
    - High Stress Detected: {vitals_data['high_stress_flag']}

    User Daily Input:
    "{user_log}"

    Task:
    Provide 2 brief, actionable, non-medical lifestyle suggestions (e.g., breathwork, light activity, diet adjustment) grounded in the retrieved context. Keep it under 100 words.
    """

    # Step C: Send request to Groq Cloud API
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error from Groq API ({response.status_code}): {response.text}"

# Quick test execution
if __name__ == "__main__":
    test_vitals = {"heart_rate_bpm": 88.5, "hrv_rmssd_ms": 18.2, "high_stress_flag": True}
    test_log = "Feeling overwhelmed today and had a huge sugary snack earlier."
    
    print("Testing LLM Agent Response...\n")
    print(generate_recommendation(test_vitals, test_log))