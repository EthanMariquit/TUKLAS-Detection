import streamlit as st
from PIL import Image
import os
import random
import requests
import time
from streamlit_lottie import st_lottie

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TUKLAS Professional",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ANIMATION LOADER ---
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Load Assets
lottie_microscope = load_lottieurl("https://lottie.host/0a927e36-6923-424d-8686-2484f4791e84/9z4s3l4Y2C.json") 
lottie_scanning = load_lottieurl("https://lottie.host/5a0c301c-6685-4841-8407-1e0078174f46/7Q1a54a72d.json") 

# --- 3. MEDICAL KNOWLEDGE BASE (Safe for Copy-Paste) ---
# Using triple quotes (""") to prevent syntax errors if lines wrap
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "🚨 CRITICAL (High Mortality Risk)",
        "cause": """Caused by Erysipelothrix rhusiopathiae. Bacteria persists in soil for years. Infection often follows sudden diet changes, stress, or ingestion of contaminated feces.""",
        "harm": """Rapid onset of high fever (40-42°C), septicemia (blood poisoning), abortion in pregnant sows, and sudden death if untreated within 24 hours.""",
        "materials": """• Penicillin (Injectable)<br>• Sterile Syringes (16G/18G)<br>• Digital Thermometer<br>• Disinfectant (Phenol-based)<br>• Isolation Pen""",
        "prevention": """• Vaccinate breeding herd twice yearly.<br>• Quarantine new animals for 30 days.<br>• Ensure proper disposal of infected bedding.""",
        "steps": [
            "IMMEDIATE: Isolate the affected animal to prevent herd spread.",
            "TREATMENT: Administer Penicillin (1mL/10kg BW) intramuscularly every 12-24 hours.",
            "SUPPORT: Provide electrolytes in water to combat dehydration.",
            "MONITOR: Check temperature twice daily until fever subsides."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange
