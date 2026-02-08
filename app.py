import streamlit as st
from PIL import Image
import os
import random
import requests
import time
from streamlit_lottie import st_lottie
from fpdf import FPDF  # <--- NEW LIBRARY FOR PDF
import datetime

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

# --- 2.5 CUSTOM BOX FUNCTIONS (Unified Style) ---
def custom_box(text, color_class):
    st.markdown(f'<div class="{color_class}">{text.strip()}</div>', unsafe_allow_html=True)

def st_purple(text): custom_box(text, "purple-box")
def st_blue(text):   custom_box(text, "blue-box")
def st_red(text):    custom_box(text, "red-box")
def st_yellow(text): custom_box(text, "yellow-box")
def st_green(text):  custom_box(text, "green-box")

# Load Assets
lottie_microscope = load_lottieurl("https://lottie.host/0a927e36-6923-424d-8686-2484f4791e84/9z4s3l4Y2C.json") 
lottie_scanning = load_lottieurl("https://lottie.host/5a0c301c-6685-4841-8407-1e0078174f46/7Q1a54a72d.json") 

# --- 3. MEDICAL KNOWLEDGE BASE ---
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "🚨 CRITICAL (High Mortality Risk)",
        "cause": "Caused by Erysipelothrix rhusiopathiae. Bacteria persists in soil for years. Infection often follows sudden diet changes, stress, or ingestion of contaminated feces.",
        "harm": "Rapid onset of high fever (40-42°C), septicemia (blood poisoning), abortion in pregnant sows, and sudden death if untreated within 24 hours.",
        "materials": "- Penicillin (Injectable)\n- Sterile Syringes (16G/18G)\n- Digital Thermometer\n- Disinfectant (Phenol-based)\n- Isolation Pen",
        "prevention": """- Vaccinate breeding herd twice yearly.
- Quarantine new animals for 30 days.
- Ensure proper disposal of infected bedding.""",
        "steps": [
            "IMMEDIATE: Isolate the affected animal to prevent herd spread.",
            "TREATMENT: Administer Penicillin (1mL/10kg BW) intramuscularly every 12-24 hours.",
            "SUPPORT: Provide electrolytes in water to combat dehydration.",
            "MONITOR: Check temperature twice daily until fever subsides."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange)": {
        "severity": "⚠️ MODERATE (Chronic / Contagious)",
        "cause": "Caused by the mite Sarcoptes scabiei var. suis. The mite burrows into the skin to lay eggs. Highly contagious via direct contact or shared rubbing posts.",
        "harm": "Intense itching causes weight loss, poor feed conversion efficiency (FCR), and secondary bacterial infections from scratching open wounds.",
        "materials": "- Ivermectin or Doramectin\n- Knapsack Sprayer (for amitraz)\n- Skin Scraping Kit (Scalpel/Slide)\n- Protective Gloves",
        "prevention": """- Treat sows 7-14 days before farrowing.
- Treat boars every 3 months.
- Sterilize rubbing posts and walls.""",
        "steps": [
            "INJECT: Administer Ivermectin (1mL/33kg BW) subcutaneously.",
            "SPRAY: Apply Amitraz solution to the entire herd (not just the sick pig).",
            "REPEAT: Repeat treatment after 14 days to kill newly hatched eggs.",
            "CLEAN: Scrub the pig with mild soap to remove crusts before spraying."
        ]
    },
    "Greasy / Exudative Skin (Greasy Pig Disease)": {
        "severity": "⚠️ HIGH (Especially in Piglets)",
        "cause": "Caused by Staphylococcus hyicus. Bacteria enters through skin abrasions caused by fighting (needle teeth), rough concrete, or mange bites.",
        "harm": "Toxins damage the liver and kidneys. Piglets become dehydrated rapidly due to skin fluid loss. Mortality can reach 90% in severe litters.",
        "materials": "- Antibiotics (Amoxicillin/Lincomycin)\n- Antiseptic Soap (Betadine/Chlorhexidine)\n- Soft Cloths\n- Electrolyte Solution",
        "prevention": """- Clip 'needle teeth' of piglets within 24 hours.
- Provide soft bedding (rice hull) to prevent abrasions.
- Maintain strict hygiene in farrowing crates.""",
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
        "materials": "- Routine Vitamins (B-Complex)\n- Vaccination Schedule Record\n- Standard Cleaning Supplies",
        "prevention": """- Continue current vaccination program.
- Maintain regular deworming schedule.
- Monitor feed intake daily.""",
        "steps": [
            "MAINTENANCE: Continue providing clean water and balanced feed.",
            "MONITORING: Observe for any changes in appetite or activity.",
            "RECORD: Log the healthy status in your farm inventory."
        ]
    }
}

# --- 4. PDF GENERATOR ENGINE ---
class PDFReport(FPDF):
    def header(self):
        # Header Color
        self.set_fill_color(0, 86, 179) # Blue
        self.rect(0, 0, 210, 40, 'F')
        
        # Title
        self.set_font('Arial', 'B', 24)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, 'TUKLAS DIAGNOSTICS', 0, 1, 'C')
        
        # Subtitle
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, 'Veterinary Skin Lesion Analysis System | RiSci Research', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Disclaimer: This is an AI-generated report. Consult a licensed veterinarian for final diagnosis.', 0, 0, 'C')

def create_pdf(img_path, diagnosis, confidence, info):
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. CASE DETAILS
    pdf.set_text_color(0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
    pdf.cell(0, 10, f"Case ID: #TK-{random.randint(1000,9999)}", 0, 1, 'R')
    pdf.ln(5)
    
    # 2. IMAGE
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "SPECIMEN ANALYSIS", 0, 1, 'L')
    try:
        # Centering Image
        img_width = 100
        x_pos = (210 - img_width) / 2
        pdf.image(img_path, x=x_pos, w=img_width)
        pdf.ln(5)
    except:
        pdf.cell(0, 10, "[Image Error]", 0, 1)

    # 3. DIAGNOSIS BOX
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, pdf.get_y(), 190, 35, 'F')
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(20)
    pdf.cell(50, 10, "DETECTED:", 0, 0)
    pdf.set_text_color(200, 0, 0) # Red
    pdf.cell(0, 10, diagnosis.upper(), 0, 1)
    
    pdf.set_text_color(0)
    pdf.cell(20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "CONFIDENCE:", 0, 0)
    pdf.cell(0, 10, f"{confidence:.1f}%", 0, 1)
    
    pdf.cell(20)
    pdf.cell(50, 10, "SEVERITY:", 0, 0)
    # Handle severity text to fit
    sev_text = info['severity'][:60] + "..." if len(info['severity']) > 60 else info['severity']
    pdf.cell(0, 10, sev_text, 0, 1)
    pdf.ln(10)
    
    # 4. TREATMENT PROTOCOL
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 86, 179)
    pdf.cell(0, 10, "RECOMMENDED TREATMENT PROTOCOL", 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Line
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0)
    
    for step in info['steps']:
        # Clean text for PDF (remove emojis sometimes causes issues in basic FPDF)
        clean_step = step.encode('latin-1', 'replace').decode('latin-1') 
        pdf.multi_cell(0, 8, f"- {clean_step}")
        pdf.ln(1)
        
    return pdf.output(dest='S').encode('latin-1')

# --- 5. REPORT GENERATOR HELPER ---
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
        return (f"Analysis complete. The system detected <b>{count} region(s)</b> classified as "
                f"<b>Healthy Skin</b>. With a confidence of <b>{confidence:.1f}%</b>, the animal "
                "appears free of visible pathologies.")

    text = f"{random.choice(intros)} {random.choice(descriptions)} {random.choice(actions)}"
    return text

# --- 6. CONTACTS DATA ---
contacts_data = [
    {"LGU": "Angono", "Office": "Municipal Veterinary Office", "Head": "Dr. Joel V. Tuplano", "Contact": "(02) 8451-1033", "Email": "officeofthemayor.angono@gmail.com"},
    {"LGU": "Antipolo City", "Office": "City Veterinary Office", "Head": "Dr. Rocelle D. Pico", "Contact": "(02) 8689-4514", "Email": "antipolocityvet@gmail.com"},
    {"LGU": "Baras", "Office": "Municipal Agriculture Office", "Head": "Mr. Jonathan Argueza", "Contact": "0920-958-1068", "Email": "lgubarasrizal@gmail.com"},
    {"LGU": "Binangonan", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8234-2124", "Email": "agriculture@binangonan.gov.ph"},
    {"LGU": "Cainta", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8696-2583", "Email": "agriculture@cainta.gov.ph"},
    {"LGU": "Cardona", "Office": "Municipal Agriculture Office", "Head": "Mr. Pocholo F. Raymundo", "Contact": "(02) 8539-2399 loc 108", "Email": "josephinealegre123@gmail.com"},
    {"LGU": "Jalajala", "Office": "Municipal Agriculture Office", "Head": "Engr. Aldrin T. Albos", "Contact": "(02) 8654-0447", "Email": "jalajala.lgu@gmail.com"},
    {"LGU": "Morong", "Office": "Municipal Agriculture Office", "Head": "Engr. Arlene T. Esmama", "Contact": "(02) 8236-0428", "Email": "morongrizal.agri@gmail.com"},
    {"LGU": "Pililla", "Office": "Municipal Agriculture Office", "Head": "Mr. Joseph Salvador B. Jarcia", "Contact": "Walk-in Recommended", "Email": "agriculturepililia@gmail.com"},
    {"LGU": "San Mateo", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8297-8100 loc 121", "Email": "agri.sanmateo@gmail.com"},
    {"LGU": "Montalban", "Office": "Municipal Agriculture Office", "Head": "Dr. Isagani G. Serrano", "Contact": "(02) 8941-2365", "Email": "agriculture@montalban.gov.ph"},
    {"LGU": "Tanay", "Office": "Municipal Agriculture Office", "Head": "Mr. Romeo B. Cruz", "Contact": "(02) 8655-1773", "Email": "tanay.agri@gmail.com"},
    {"LGU": "Taytay", "Office": "Municipal Agriculture Office", "Head": "Dr. Ramsen S. Andres", "Contact": "(02) 8284-4700", "Email": "agriculture@taytayrizal.gov.ph"},
    {"LGU": "Teresa", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "Walk-in Recommended", "Email": "agriculture@teresarizal.gov.ph"},
]

# --- 7. CSS STYLING (THEMED) ---
st.markdown("""
    <style>
    /* REMOVE HARDCODED MAIN BACKGROUND SO STREAMLIT THEME WORKS */
    .stApp {
        /* No specific background set here to allow dark mode to work */
    }
    
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        border: none;
    }

    /* --- CUSTOM BOX STYLES --- */
    .purple-box, .blue-box, .red-box, .yellow-box, .green-box {
        padding: 16px;
        border-radius: 5px;
        color: inherit; 
        font-family: 'Source Sans Pro', sans-serif;
        margin-bottom: 10px;
        white-space: pre-wrap;
        line-height: 1.5; 
    }
    .purple-box { background-color: rgba(106, 13, 173, 0.1); border: 1px solid #6A0DAD; }
    .blue-box { background-color: rgba(0, 86, 179, 0.1); border: 1px solid #0056b3; }
    .red-box { background-color: rgba(255, 75, 75, 0.1); border: 1px solid #FF4B4B; }
    .yellow-box { background-color: rgba(255, 170, 0, 0.1); border: 1px solid #FFAA00; }
    .green-box { background-color: rgba(0, 200, 83, 0.1); border: 1px solid #00C853; }

    /* REPORT BOX */
    .report-box {
        background-color: rgba(255, 255, 255, 0.05);
        color: inherit;
        padding: 25px 25px 50px 25px; 
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid #0056b3;
        border: 1px solid rgba(128, 128, 128, 0.2);
        font-size: 16px;
        line-height: 1.6;
        margin-bottom: 10px;
    }
    
    .proto-header {
        color: #0056b3;
        font-weight: bold;
        font-size: 1.1em;
        margin-bottom: 5px;
        margin-top: 10px;
    }
    
    /* FOOTER */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2c3e50;
        color: #ecf0f1;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        z-index: 100;
        border-top: 3px solid #0056b3;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 8. MODEL LOADING ---
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

# --- 9. SIDEBAR ---
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
        st.info("ℹ️ **Usage Guide**\n1. Upload a clear image of the skin.\n2. The AI will highlight anomalies.\n3. Download the official PDF Report.")

# --- 10. PAGE: LESION SCANNER ---
if selected_page == "🔍 Lesion Scanner":
    st.title("🔬 TUKLAS: Smart Veterinary Assistant")
    st.write("Upload a sample image to generate a diagnostic report.")

    # File Uploader
    uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        
        # Save temp image for PDF generation
        with open("temp_analysis.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

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
                        st.metric(label="AI Confidence Score", value=f"{confidence:.1f}%")
                        st.progress(int(confidence))

                st.markdown("---")
                if count == 0:
                    st_green("✅ <b>Negative Result:</b> No skin lesions detected.")
                else:
                    det_class = unique_detections[0] 
                    report = generate_smart_report(det_class, count, confidence)
                    
                    # Get Medical Info for PDF
                    info = medical_data.get(det_class)
                    if not info:
                         for k in medical_data.keys():
                            if k in det_class or det_class in k:
                                info = medical_data[k]
                                break

                    # --- WRAPPED REPORT ---
                    with st.expander("📋 AI DIAGNOSTIC REPORT", expanded=True):
                        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
                        
                        # === NEW: DOWNLOAD BUTTON ===
                        if info:
                            pdf_bytes = create_pdf("temp_analysis.jpg", det_class, confidence, info)
                            st.download_button(
                                label="📥 Download Official Lab Report (PDF)",
                                data=pdf_bytes,
                                file_name=f"TUKLAS_Report_{int(time.time())}.pdf",
                                mime="application/pdf"
                            )
                        # ============================
                    
                    st.write("") 

                    # --- DETAILED PROTOCOL SECTION ---
                    for d in unique_detections:
                        # Re-fetch info inside loop for display
                        d_info = medical_data.get(d)
                        if not d_info:
                            for k in medical_data.keys():
                                if k in d or d in k:
                                    d_info = medical_data[k]
                                    break
                        
                        if d_info:
                            with st.expander(f"📌 PROTOCOL: {d}", expanded=True):
                                # SECTION 1
                                st.markdown(f'<p style="margin-bottom: 0px;"><b>SEVERITY STATUS:</b> <code>{d_info["severity"]}</code></p>', unsafe_allow_html=True)
                                st.divider()
                                
                                # SECTION 2
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown('<p class="proto-header">🧬 Origin & Transmission</p>', unsafe_allow_html=True)
                                    st_blue(d_info['cause']) 
                                with c2:
                                    st.markdown('<p class="proto-header">💔 Clinical Impact</p>', unsafe_allow_html=True)
                                    st_red(d_info['harm']) 
                                
                                # SECTION 3
                                c3, c4 = st.columns(2)
                                with c3:
                                    st.markdown('<p class="proto-header">🧰 Required Supplies</p>', unsafe_allow_html=True)
                                    st_yellow(d_info['materials']) 
                                with c4:
                                    st.markdown('<p class="proto-header">🛡️ Bio-Security & Prevention</p>', unsafe_allow_html=True)
                                    st_purple(d_info["prevention"])
                                
                                st.divider()
                                
                                # SECTION 4
                                st.markdown('<p class="proto-header">💊 Treatment Protocol</p>', unsafe_allow_html=True)
                                protocol_text = ""
                                for step in d_info['steps']:
                                    protocol_text += f"✅ {step}\n"
                                st_green(protocol_text) 

# --- 11. PAGE: DIRECTORY ---
elif selected_page == "📞 Local Directory":
    st.title("📞 Agricultural Support Directory")
    search_term = st.text_input("🔍 Search Municipality", "")
    st.markdown("---")

    col1, col2 = st.columns(2)
    # Re-inserting the contact list logic here 
    visible = [c for c in contacts_data if search_term.lower() in c['LGU'].lower() or search_term == ""]
    
    if len(visible) == 0:
        st_yellow("No offices found matching your search.")

    for i, data in enumerate(visible):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"📍 **{data['LGU']}**", expanded=True):
                st.write(f"**Office:** {data['Office']}")
                st.write(f"**Head:** {data['Head']}")
                st.write(f"**Phone:** `{data['Contact']}`")
                st.write(f"**Email:** {data['Email']}")

# --- 12. FOOTER ---
st.markdown("""
<div class="footer">
    <p><strong>Rizal National Science High School (RiSci)</strong><br>
    📍 J.P. Rizal St., Batingan, Binangonan, Rizal<br>
    📞 (02) 8652-2197 | ✉️ rnshs.admin@deped.gov.ph<br>
    © 2025 Student Research Project | TUKLAS Team</p>
</div>
""", unsafe_allow_html=True)
