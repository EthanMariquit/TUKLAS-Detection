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

# --- 2. ANIMATION LOADER (With Safety Check) ---
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
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5tkzkblw.json") 

# --- 3. MEDICAL KNOWLEDGE BASE ---
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "🚨 CRITICAL (High Mortality Risk)",
        "cause": "Caused by <i>Erysipelothrix rhusiopathiae</i>. Bacteria persists in soil for years. Infection often follows sudden diet changes, stress, or ingestion of contaminated feces.",
        "harm": "Rapid onset of high fever (40-42°C), septicemia (blood poisoning), abortion in pregnant sows, and sudden death if untreated within 24 hours.",
        "materials": "• Penicillin (Injectable)<br>• Sterile Syringes (16G/18G)<br>• Digital Thermometer<br>• Disinfectant (Phenol-based)<br>• Isolation Pen",
        "prevention": "• Vaccinate breeding herd twice yearly.<br>• Quarantine new animals for 30 days.<br>• Ensure proper disposal of infected bedding.",
        "steps": [
            "IMMEDIATE: Isolate the affected animal to prevent herd spread.",
            "TREATMENT: Administer Penicillin (1mL/10kg BW) intramuscularly every 12-24 hours.",
            "SUPPORT: Provide electrolytes in water to combat dehydration.",
            "MONITOR: Check temperature twice daily until fever subsides."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange)": {
        "severity": "⚠️ MODERATE (Chronic / Contagious)",
        "cause": "Caused by the mite <i>Sarcoptes scabiei var. suis</i>. The mite burrows into the skin to lay eggs. Highly contagious via direct contact or shared rubbing posts.",
        "harm": "Intense itching causes weight loss, poor feed conversion efficiency (FCR), and secondary bacterial infections from scratching open wounds.",
        "materials": "• Ivermectin or Doramectin<br>• Knapsack Sprayer (for amitraz)<br>• Skin Scraping Kit (Scalpel/Slide)<br>• Protective Gloves",
        "prevention": "• Treat sows 7-14 days before farrowing to protect piglets.<br>• Treat boars every 3 months.<br>• Sterilize rubbing posts and walls.",
        "steps": [
            "INJECT: Administer Ivermectin (1mL/33kg BW) subcutaneously.",
            "SPRAY: Apply Amitraz solution to the entire herd (not just the sick pig).",
            "REPEAT: Repeat treatment after 14 days to kill newly hatched eggs.",
            "CLEAN: Scrub the pig with mild soap to remove crusts before spraying."
        ]
    },
    "Greasy / Exudative Skin (Greasy Pig Disease)": {
        "severity": "⚠️ HIGH (Especially in Piglets)",
        "cause": "Caused by <i>Staphylococcus hyicus</i>. Bacteria enters through skin abrasions caused by fighting (needle teeth), rough concrete, or mange bites.",
        "harm": "Toxins damage the liver and kidneys. Piglets become dehydrated rapidly due to skin fluid loss. Mortality can reach 90% in severe litters.",
        "materials": "• Antibiotics (Amoxicillin/Lincomycin)<br>• Antiseptic Soap (Betadine/Chlorhexidine)<br>• Soft Cloths<br>• Electrolyte Solution",
        "prevention": "• Clip 'needle teeth' of piglets within 24 hours of birth.<br>• Provide soft bedding (rice hull/sawdust) to prevent knee abrasions.<br>• Maintain strict hygiene in farrowing crates.",
        "steps": [
            "WASH: Gently wash the pig with antiseptic soap/solution daily.",
            "MEDICATE: Inject Amoxicillin or Lincomycin for 3-5 days.",
            "HYDRATE: Oral rehydration is critical for survival.",
            "ENVIRONMENT: Ensure the pen is dry and draft-free."
        ]
    },
    "Healthy": {
        "severity": "✅ OPTIMAL",
        "cause": "Evidence of good husbandry, proper nutrition, and effective biosecurity measures.",
        "harm": "N/A - The animal appears to be in good physical condition.",
        "materials": "• Routine Vitamins (B-Complex)<br>• Vaccination Schedule Record<br>• Standard Cleaning Supplies",
        "prevention": "• Continue current vaccination program.<br>• Maintain regular deworming schedule.<br>• Monitor feed intake daily.",
        "steps": [
            "MAINTENANCE: Continue providing clean water and balanced feed.",
            "MONITORING: Observe for any changes in appetite or activity.",
            "RECORD: Log the healthy status in your farm inventory."
        ]
    }
}

# --- 4. CREATIVE REPORT GENERATOR ---
def generate_smart_report(detected_class, count, confidence):
    intros = [
        f"Analysis of the uploaded specimen indicates the presence of <b>{count} distinct anomaly/anomalies</b>.",
        f"The TUKLAS diagnostic system has flagged <b>{count} region(s) of interest</b> in this sample.",
        f"Based on visual dermatological patterns, our AI identified <b>{count} area(s)</b> requiring attention.",
        f"A thorough scan of the tissue sample reveals <b>{count} point(s) of concern</b>."
    ]
    descriptions = [
        f"The morphological features are highly consistent with <b>{detected_class}</b>.",
        f"The AI has classified the skin texture and discoloration patterns as <b>{detected_class}</b>.",
        f"Visual indicators suggest a high probability of <b>{detected_class}</b>.",
        f"The detected lesions exhibit characteristics typical of <b>{detected_class}</b>."
    ]
    actions = [
        f"With a confidence score of <b>{confidence:.1f}%</b>, immediate veterinary assessment is recommended.",
        f"The system is <b>{confidence:.1f}%</b> certain of this diagnosis. Please refer to the treatment protocols below.",
        f"Given the high confidence (<b>{confidence:.1f}%</b>), isolation protocols should be initiated immediately.",
        f"The model's certainty is <b>{confidence:.1f}%</b>. We advise cross-referencing this with a physical exam."
    ]
    
    if "Healthy" in detected_class:
        return f"Analysis complete. The system detected <b>{count} region(s)</b> classified as <b>Healthy Skin</b>. With a confidence of <b>{confidence:.1f}%</b>, the animal appears to be free of visible dermatological pathologies. Continue routine monitoring."

    text = f"{random.choice(intros)} {random.choice(descriptions)} {random.choice(actions)}"
    return text

# --- 5. CONTACTS DATA ---
contacts_data = [
    {"LGU": "Angono", "Office": "Municipal Veterinary Office", "Head": "Dr. Joel V. Tuplano", "Contact": "(02) 8451-1033", "Email": "officeofthemayor.angono@gmail.com"},
    {"LGU": "Antipolo City", "Office": "City Veterinary Office", "Head": "Dr. Rocelle D. Pico", "Contact": "(02) 8689-4514", "Email": "antipolocityvet@gmail.com"},
    {"LGU": "Baras", "Office": "Municipal Agriculture Office", "Head": "Mr. Jonathan Argueza", "Contact": "0920-958-1068", "Email": "lgubarasrizal@gmail.com"},
    {"LGU": "Binangonan", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8234-2124", "Email": "agriculture@binangonan.gov.ph"},
    {"LGU": "Cainta", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8696-2583", "Email": "agriculture@cainta.gov.ph"},
    {"LGU": "Cardona", "Office": "Municipal Agriculture Office", "Head": "Mr. Pocholo F. Raymundo", "Contact": "(02) 8539-2399 loc 108", "Email": "josephinealegre123@gmail.com"},
    {"LGU": "Jalajala", "Office": "Municipal Agriculture Office", "Head": "Engr. Aldrin T. Albos", "Contact": "(02) 8654-0447", "Email": "jalajala.lgu@gmail.com"},
    {"LGU": "Morong", "Office": "Municipal Agriculture Office", "Head": "Engr. Arlene T. Esmama", "Contact": "(02) 8236-0428", "Email": "morongrizal.agri@gmail.com"},
    {"
