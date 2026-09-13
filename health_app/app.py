import streamlit as st
import requests
import numpy as np
import neurokit2 as nk

st.set_page_config(page_title="AI Health Assistant", page_icon="🫀", layout="centered")

st.title("🫀 AI Lifestyle & Vitality Assistant")
st.write("Monitor your pulse biometrics and receive tailored, non-medical lifestyle guidance.")

st.divider()

# 1. User Journal Input
st.subheader("1. Daily Check-in")
journal_entry = st.text_area(
    "How are you feeling today?", 
    placeholder="e.g., Felt a bit stressed this afternoon, had trouble sleeping last night..."
)

# 2. Simulated PPG Signal Generator
st.subheader("2. Biometric Pulse Acquisition")
st.info("Simulating a 10-second PPG sensor scan at 100Hz...")

if st.button("Generate & Analyze Vitals", type="primary"):
    if not journal_entry.strip():
        st.warning("Please enter a short journal note before running the analysis.")
    else:
        with st.spinner("Processing pulse signal & retrieving AI recommendations..."):
            try:
                # Generate a 10-second PPG signal array (1000 data points)
                simulated_ppg = nk.ppg_simulate(duration=10, sampling_rate=100, heart_rate=72)
                raw_signal_list = simulated_ppg.tolist()

                # Send request to local FastAPI backend
                payload = {
                    "raw_ppg_signal": raw_signal_list,
                    "sampling_rate": 100,
                    "journal_log": journal_entry
                }
                
                response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    biometrics = data["biometrics"]
                    recommendation = data["lifestyle_recommendation"]

                    # Display Metrics
                    st.divider()
                    st.subheader("3. Real-time Biometric Analysis")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Heart Rate", f"{biometrics['heart_rate_bpm']} BPM")
                    col2.metric("HRV (RMSSD)", f"{biometrics['hrv_rmssd_ms']} ms")
                    col3.metric("Stress Flag", "High Stress" if biometrics['high_stress_flag'] else "Normal Drive")

                    # Display Recommendation
                    st.subheader("4. Personalized Lifestyle Guidance")
                    st.markdown(recommendation)
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")

            except Exception as e:
                st.error(f"Could not connect to FastAPI server. Ensure main:app is running! Error: {str(e)}")