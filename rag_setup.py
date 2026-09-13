import chromadb

def setup_knowledge_base():
    # Persistent client saves vectors to local disk at zero cost
    client = chromadb.PersistentClient(path="./health_knowledge_db")
    collection = client.get_or_create_collection(name="lifestyle_guidelines")

    # Structured medical & lifestyle guidelines
    guidelines = [
        {
            "id": "diabetes_walking",
            "text": "Post-meal light walking (10 to 15 minutes) significantly lowers glucose spikes and improves insulin sensitivity in individuals with metabolic risks.",
            "category": "diabetes"
        },
        {
            "id": "anxiety_vagus_breathing",
            "text": "For elevated heart rate or acute anxiety, the 4-7-8 breathing exercise (inhale 4s, hold 7s, exhale 8s) stimulates the vagus nerve and lowers sympathetic drive.",
            "category": "anxiety_stress"
        },
        {
            "id": "dementia_mind_diet",
            "text": "Adhering to the MIND diet (leafy green vegetables, berries, nuts, olive oil, and limited saturated fats) helps reduce neuroinflammation and supports long-term cognitive reserve.",
            "category": "cognitive_health"
        },
        {
            "id": "cardio_hrv_recovery",
            "text": "A drop in HRV RMSSD indicates autonomic nervous system fatigue or psychological stress. Prioritize 7-8 hours of sleep and gentle somatic grounding techniques.",
            "category": "heart_hrv"
        }
    ]

    # Add guidelines to ChromaDB collection
    for doc in guidelines:
        collection.add(
            documents=[doc["text"]],
            metadatas=[{"category": doc["category"]}],
            ids=[doc["id"]]
        )

    print("Local ChromaDB successfully initialized and populated!")

if __name__ == "__main__":
    setup_knowledge_base()