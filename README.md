# AI-health-app
# 🫀 Open-Source Biometric Stress & Health Assistant

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple?style=flat)](https://www.trychroma.com/)
[![Groq Cloud](https://img.shields.io/badge/LLM-Groq%20Cloud-orange?style=flat)](https://groq.com/)

An end-to-end local health architecture that extracts heart rate and Heart Rate Variability (HRV) metrics from Photoplethysmogram (PPG) pulse signals, pairs them with daily user subjective logs, and provides personalized, non-diagnostic lifestyle guidance using Retrieval-Augmented Generation (RAG).

---

## 🌟 Key Features

* 📊 **Biometric Signal Processing:** Cleans raw PPG pulse data and calculates Heart Rate (BPM) and HRV RMSSD (ms) via `NeuroKit2`.
* 🧠 **Grounding via Vector RAG:** Embeds clinical and non-medical lifestyle guidelines into a local `ChromaDB` vector store to eliminate hallucinations.
* ⚡ **High-Speed Inference:** Connects context to `Groq Cloud API` (`openai/gpt-oss-120b`) for rapid recommendation synthesis.
* 🔌 **FastAPI REST Service:** Modular backend offering clean endpoints (`/analyze`) for pulse processing and RAG pipeline execution.
* 💻 **Streamlit Interactive UI:** Functional dashboard for real-time PPG simulation, daily check-in logs, and metric visualizers.

---

## 🏗️ System Architecture

```text
┌─────────────────┐      ┌─────────────────────────┐      ┌──────────────────────────┐
│ Streamlit UI    │ ───> │ FastAPI Server          │ ───> │ NeuroKit2 Engine         │
│ (User Inputs)   │      │ (POST /analyze)         │      │ (PPG & HRV Metrics)      │
└─────────────────┘      └─────────────────────────┘      └──────────────────────────┘
                                      │                                 │
                                      ▼                                 │
                         ┌─────────────────────────┐                    │
                         │ ChromaDB (Local RAG)    │ <──────────────────┘
                         │ (Clinical Context)      │
                         └─────────────────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │ Groq Cloud API          │
                         │ (LLM Recommendation)    │
                         └─────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.10+
* Free [Groq Cloud API Key](https://console.groq.com/)

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/biometric-health-assistant.git](https://github.com/YOUR_USERNAME/biometric-health-assistant.git)
   cd biometric-health-assistant
   ```

2. **Set up virtual environment:**
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux/macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize local ChromaDB Vector Store:**
   ```bash
   python rag_setup.py
   ```

5. **Set up API key:**
   Add your Groq API key inside `llm_agent.py`:
   ```python
   GROQ_API_KEY = "your_actual_groq_api_key"
   ```

---

## 🏃 Running the Application

### 1. Launch FastAPI Backend
In your primary terminal window:
```powershell
uvicorn main:app --reload
```
*Docs will be accessible at: `http://127.0.0.1:8000/docs`*

### 2. Launch Streamlit UI
In a second active terminal window:
```powershell
streamlit run app.py
```
*UI will open in browser at: `http://localhost:8501`*

---

## 🛠️ Project Structure

```text
health_app_backend/
│
├── signal_processor.py   # PPG pulse cleaning & HRV metric extraction
├── rag_setup.py          # ChromaDB initialization & vector embedding pipeline
├── llm_agent.py          # Vector search query & Groq API LLM integration
├── main.py               # FastAPI REST endpoints
├── app.py                # Streamlit user interface
├── requirements.txt      # Dependency list
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation
```

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for details.
