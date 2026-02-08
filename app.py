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
lottie_success = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_5tkzkblw.json") 

# --- 3. MEDICAL KNOWLEDGE BASE ---
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "🚨 CRITICAL (High Mortality Risk)",
        "cause": "Caused by <i>Erysipelothrix rhusiopathiae</i>. Bacteria persists in soil for years. Infection often follows sudden diet changes.",
        "harm": "Rapid onset of high fever (40-42°C), septicemia (blood poisoning), and sudden death if untreated within 24 hours.",
        "materials": "• Penicillin (Injectable)<br>• Sterile Syringes (16G/18G)<br>• Digital Thermometer<br>• Disinfectant",
        "prevention": "• Vaccinate breeding herd twice yearly.<br>• Quarantine new animals for 30 days.",
        "steps": [
            "IMMEDIATE: Isolate the affected animal to prevent herd spread.",
            "TREATMENT: Administer Penicillin (1mL/10kg BW) intramuscularly every 12-24 hours.",
            "SUPPORT: Provide electrolytes in water to combat dehydration.",
            "MONITOR: Check temperature twice daily until fever subsides."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange)": {
        "severity": "⚠️ MODERATE (Chronic / Contagious)",
        "cause": "Caused by the mite <i>Sarcoptes scabiei var. suis</i>. Highly contagious via direct contact.",
        "harm": "Intense itching causes weight loss, poor feed conversion efficiency (FCR), and secondary bacterial infections.",
        "materials": "• Ivermectin or Doramectin<br>• Knapsack Sprayer<br>• Skin Scraping Kit<br>• Protective Gloves",
        "prevention": "• Treat sows 7-14 days before farrowing.<br>• Treat boars every 3 months.<br>• Sterilize rubbing posts.",
        "steps": [
            "INJECT: Administer Ivermectin (1mL/33kg BW) subcutaneously.",
            "SPRAY: Apply Amitraz solution to the entire herd.",
            "REPEAT: Repeat treatment after 14 days to kill newly hatched eggs.",
            "CLEAN: Scrub the pig with mild soap to remove crusts before spraying."
        ]
    },
    "Greasy / Exudative Skin (Greasy Pig Disease)": {
        "severity": "⚠️ HIGH (Especially in Piglets)",
        "cause": "Caused by <i>Staphylococcus hyicus</i>. Bacteria enters through skin abrasions caused by fighting.",
        "harm": "Toxins damage the liver and kidneys. Piglets become dehydrated rapidly due to skin fluid loss.",
        "materials": "• Antibiotics (Amoxicillin)<br>• Antiseptic Soap (Betadine)<br>• Soft Cloths<br>• Electrolyte Solution",
        "prevention": "• Clip 'needle teeth' of piglets within 24 hours of birth.<br>• Provide soft bedding.<br>• Maintain strict hygiene.",
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
        "prevention": "• Continue current vaccination program.<br>• Maintain regular deworming schedule.",
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
        f"Analysis indicates <b>{count} distinct anomaly/anomalies</b>.",
        f"TUKLAS system flagged <b>{count} region(s) of interest</b>.",
        f"We identified <b>{count} area(s)</b> requiring attention.",
        f"Scan reveals <b>{count} point(s) of concern</b>."
    ]
    descriptions = [
        f"Features are consistent with <b>{detected_class}</b>.",
        f"Patterns resemble <b>{detected_class}</b>.",
        f"Visual indicators suggest <b>{detected_class}</b>.",
        f"Lesions exhibit characteristics of <b>{detected_class}</b>."
    ]
    actions = [
        f"Confidence: <b>{confidence:.1f}%</b>. Veterinary assessment recommended.",
        f"Certainty: <b>{confidence:.1f}%</b>. See treatment protocols below.",
        f"Confidence: <b>{confidence:.1f}%</b>. Isolation protocols advised.",
        f"Certainty: <b>{confidence:.1f}%</b>. Cross-reference with physical exam."
    ]
    
    if "Healthy" in detected_class:
        return (f"Analysis complete. The system detected <b>{count} region(s)</b> classified as "
                f"<b>Healthy Skin</b>. With a confidence of <b>{confidence:.1f}%</b>, the animal "
                "appears free of visible pathologies.")

    text = f"{random.choice(intros)} {random.choice(descriptions)} {random.choice(actions)}"
    return text

# --- 5. CONTACTS DATA ---
contacts_data = [
    {"LGU": "Angono", "Office": "Municipal Vet", "Head": "Dr. Joel V. Tuplano", "Contact": "(02) 8451-1033", "Email": "officeofthemayor.angono@gmail.com"},
    {"LGU": "Antipolo", "Office": "City Vet", "Head": "Dr. Rocelle D. Pico", "Contact": "(02) 8689-4514", "Email": "antipolocityvet@gmail.com"},
    {"LGU": "Baras", "Office": "Agriculture Office", "Head": "Mr. Jonathan Argueza", "Contact": "0920-958-1068", "Email": "lgubarasrizal@gmail.com"},
    {"LGU": "Binangonan", "Office": "Agriculture Office", "Head": "Dept. Head", "Contact": "(02) 8234-2124", "Email": "agriculture@binangonan.gov.ph"},
    {"LGU": "Cainta", "Office": "Agriculture Office", "Head": "Dept. Head", "Contact": "(02) 8696-2583", "Email": "agriculture@cainta.gov.ph"},
    {"LGU": "Cardona", "Office": "Agriculture Office", "Head": "Mr. Pocholo F. Raymundo", "Contact": "(02) 8539-2399", "Email": "josephinealegre123@gmail.com"},
    {"LGU": "Jalajala", "Office": "Agriculture Office", "Head": "Engr. Aldrin T. Albos", "Contact": "(02) 8654-0447", "Email": "jalajala.lgu@gmail.com"},
    {"LGU": "Morong", "Office": "Agriculture Office", "Head": "Engr. Arlene T. Esmama", "Contact": "(02) 8236-0428", "Email": "morongrizal.agri@gmail.com"},
    {"LGU": "Pililla", "Office": "Agriculture Office", "Head": "Mr. Joseph Salvador B. Jarcia", "Contact": "Walk-in", "Email": "agriculturepililia@gmail.com"},
    {"LGU": "San Mateo", "Office": "Agriculture Office", "Head": "Dept. Head", "Contact": "(02) 8297-8100", "Email": "agri.sanmateo@gmail.com"},
    {"LGU": "Montalban", "Office": "Agriculture Office", "Head": "Dr. Isagani G. Serrano", "Contact": "(02) 8941-2365", "Email": "agriculture@montalban.gov.ph"},
    {"LGU": "Tanay", "Office": "Agriculture Office", "Head": "Mr. Romeo B. Cruz", "Contact": "(02) 8655-1773", "Email": "tanay.agri@gmail.com"},
    {"LGU": "Taytay", "Office": "Agriculture Office", "Head": "Dr. Ramsen S. Andres", "Contact": "(02) 8284-4700", "Email": "agriculture@taytayrizal.gov.ph"},
    {"LGU": "Teresa", "Office": "Agriculture Office", "Head": "Dept. Head", "Contact": "Walk-in", "Email": "agriculture@teresarizal.gov.ph"},
]

# --- 6. CSS STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        border: none;
    }
    .report-box {
        background-color: #ffffff;
        color: #333333; 
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid #0056b3;
        font-size: 16px;
    }
    .purple-box {
        background-color: #f3e5f5;
        color: #333333;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #9c27b0;
        margin-bottom: 10px;
        font-size: 14px;
    }
    .proto-header {
        color: #0056b3;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 7. MODEL LOADING ---
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

try:
    from ultralytics import YOLO
except ImportError:
    st.error("❌ System Error: Libraries missing.")
    st.stop()

if not os.path.exists(model_path):
    st.warning("⚠️ Model not found. Please upload best.pt")
    model = None
else:
    @st.cache_resource
    def load_model():
        return YOLO(model_path)
    model = load_model()

# --- 8. SIDEBAR ---
with st.sidebar:
    if lottie_microscope:
        st_lottie(lottie_microscope, height=150, key="sidebar_anim")
    else:
        st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
        
    st.title("TUKLAS Diagnostics")
    st.caption("Veterinary Skin Lesion Analysis System")
    st.markdown("---")
    
    selected_page = st.selectbox("Navigate", ["🔍 Lesion Scanner", "📞 Local Directory"])
    st.markdown("---")

    conf_threshold = 0.25
    if selected_page == "🔍 Lesion Scanner":
        st.write("⚙️ **Scanner Settings**")
        conf_threshold = st.slider("Sensitivity", 0.0, 1.0, 0.40, 0.05)

# --- 9. PAGE: LESION SCANNER ---
if selected_page == "🔍 Lesion Scanner":
    st.title("🔬 TUKLAS: Smart Veterinary Assistant")
    st.write("Upload a sample image to generate a diagnostic report.")

    # File Uploader with Label
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(img, use_column_width=True, caption="Uploaded Specimen")

        if st.button("🔍 Generate Report"):
            if model is None:
                st.error("Model file missing.")
            else:
                with st.spinner("Analyzing..."):
                    with col2:
                        if lottie_scanning:
                            st_lottie(lottie_scanning, height=200, key="scanning")
                    
                    # Run AI
                    results = model.predict(img, conf=conf_threshold)
                    result_plot = results[0].plot()
                    
                    detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
                    unique_detections = list(set(detected_classes))
                    count = len(detected_classes)
                    
                    confidence = 0.0
                    if len(results[0].boxes) > 0:
                        confs = results[0].boxes.conf.tolist()
                        confidence = (sum(confs) / len(confs)) * 100

                with col2:
                    st.empty()
                    st.image(result_plot, use_column_width=True, caption="AI Analysis")
                    if count > 0:
                        st.progress(int(confidence))

                st.markdown("---")
                if count == 0:
                    st.success("✅ **Negative Result:** No skin lesions detected.")
                else:
                    det_class = unique_detections[0] 
                    report = generate_smart_report(det_class, count, confidence)
                    st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                    st.write("") 

                    for d in unique_detections:
                        info = medical_data.get(d)
                        if not info:
                            # Fallback search
                            for k in medical_data.keys():
                                if k in d or d in k:
                                    info = medical_data[k]
                                    break
                        
                        if info:
                            with st.expander(f"📌 PROTOCOL: {d}", expanded=True):
                                st.markdown(f"**SEVERITY:** `{info['severity']}`")
                                st.divider()
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown('<p class="proto-header">🧬 Origin</p>', unsafe_allow_html=True)
                                    st.info(info['cause'])
                                with c2:
                                    st.markdown('<p class="proto-header">💔 Impact</p>', unsafe_allow_html=True)
                                    st.error(info['harm'])
                                
                                st.markdown('<p class="proto-header">💊 Treatment</p>', unsafe_allow_html=True)
                                p_text = "\n".join([f"✅ {s}" for s in info['steps']])
                                st.success(p_text)

# --- 10. PAGE: DIRECTORY ---
elif selected_page == "📞 Local Directory":
    st.title("📞 Agricultural Support Directory")
    search_term = st.text_input("🔍 Search Municipality", "")
    st.markdown("---")

    col1, col2 = st.columns(2)
    visible = [c for c in contacts_data if search_term.lower() in c['LGU'].lower() or search_term == ""]
    
    for i, data in enumerate(visible):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"📍 **{data['LGU']}**", expanded=True):
                st.write(f"**Office:** {data['Office']}")
                st.write(f"**Head:** {data['Head']}")
                st.write(f"**Phone:** `{data['Contact']}`")
                st.write(f"**Email:** {data['Email']}")
