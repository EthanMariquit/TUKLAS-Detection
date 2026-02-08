import streamlit as st
from PIL import Image
import os
import random
import requests
import time
from streamlit_lottie import st_lottie
from fpdf import FPDF
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TUKLAS Professional",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ASSETS & HELPERS ---
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code != 200: return None
        return r.json()
    except: return None

# Custom CSS containers
def custom_box(text, color_class):
    st.markdown(f'<div class="{color_class}">{text.strip()}</div>', unsafe_allow_html=True)

def st_purple(text): custom_box(text, "purple-box")
def st_blue(text):   custom_box(text, "blue-box")
def st_red(text):    custom_box(text, "red-box")
def st_yellow(text): custom_box(text, "yellow-box")
def st_green(text):  custom_box(text, "green-box")

lottie_microscope = load_lottieurl("https://lottie.host/0a927e36-6923-424d-8686-2484f4791e84/9z4s3l4Y2C.json") 
lottie_scanning = load_lottieurl("https://lottie.host/5a0c301c-6685-4841-8407-1e0078174f46/7Q1a54a72d.json") 

# --- 3. MEDICAL KNOWLEDGE BASE ---
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "CRITICAL (High Mortality Risk)",
        "cause": "Erysipelothrix rhusiopathiae bacteria. Persists in soil/feces. Infection follows stress or sudden diet changes.",
        "harm": "High fever (40-42C), septicemia, abortion in sows, and sudden death if untreated.",
        "materials": "Penicillin (Injectable), Sterile Syringes, Digital Thermometer, Disinfectant.",
        "prevention": "Vaccinate herd twice yearly. Quarantine new stock. Disinfect bedding.",
        "steps": [
            "Isolate the affected animal immediately.",
            "Administer Penicillin (1mL/10kg BW) intramuscularly every 12-24 hours.",
            "Provide electrolytes in water to combat dehydration.",
            "Monitor temperature twice daily until fever subsides."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange)": {
        "severity": "MODERATE (Highly Contagious)",
        "cause": "Sarcoptes scabiei var. suis mite. Burrows into skin to lay eggs. Spreads via direct contact.",
        "harm": "Intense itching, weight loss, poor feed conversion, secondary infections.",
        "materials": "Ivermectin/Doramectin, Amitraz Spray, Skin Scraping Kit.",
        "prevention": "Treat sows pre-farrowing. Treat boars quarterly. Sterilize rubbing posts.",
        "steps": [
            "Administer Ivermectin (1mL/33kg BW) subcutaneously.",
            "Apply Amitraz solution to the entire herd.",
            "Repeat treatment after 14 days to kill newly hatched eggs.",
            "Scrub animal with mild soap to remove crusts before spraying."
        ]
    },
    "Greasy / Exudative Skin (Greasy Pig Disease)": {
        "severity": "HIGH (Severe in Piglets)",
        "cause": "Staphylococcus hyicus. Enters through abrasions from fighting or rough concrete.",
        "harm": "Toxins damage liver/kidneys. Rapid dehydration and high mortality in piglets.",
        "materials": "Amoxicillin/Lincomycin, Antiseptic Soap, Electrolytes.",
        "prevention": "Clip needle teeth. Provide soft bedding. Maintain strict hygiene.",
        "steps": [
            "Wash pig with antiseptic soap/solution daily.",
            "Inject Amoxicillin or Lincomycin for 3-5 days.",
            "Ensure oral rehydration is provided immediately.",
            "Keep pen dry and draft-free."
        ]
    },
    "Healthy": {
        "severity": "OPTIMAL",
        "cause": "Evidence of good husbandry and effective biosecurity.",
        "harm": "None observed.",
        "materials": "Routine Vitamins, Vaccination Record.",
        "prevention": "Continue current vaccination and deworming program.",
        "steps": [
            "Continue providing clean water and balanced feed.",
            "Observe for any changes in appetite.",
            "Log healthy status in farm records."
        ]
    }
}

# --- 4. PROFESSIONAL PDF ENGINE ---
def clean_text(text):
    """Sanitizes text for PDF generation (removes emojis/special chars)."""
    if not isinstance(text, str): return str(text)
    # Replace common issues manually first
    text = text.replace("🚨", "").replace("⚠️", "").replace("✅", "")
    return text.encode('latin-1', 'ignore').decode('latin-1')

class PDFReport(FPDF):
    def header(self):
        # Professional Header Bar
        self.set_fill_color(30, 58, 138) # Navy Blue
        self.rect(0, 0, 210, 35, 'F')
        
        # Title
        self.set_font('Arial', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 8)
        self.cell(0, 10, 'TUKLAS DIAGNOSTICS LABORATORY', 0, 1, 'L')
        
        # Subtitle details
        self.set_font('Arial', '', 9)
        self.set_xy(10, 18)
        self.cell(0, 5, 'Rizal National Science High School | Integrated Research Dept.', 0, 1, 'L')
        self.cell(0, 5, 'JP Rizal St., Batingan, Binangonan, Rizal | Phone: (02) 8652-2197', 0, 1, 'L')
        
        # "OFFICIAL REPORT" Stamp text on right
        self.set_font('Arial', 'B', 14)
        self.set_text_color(200, 200, 200)
        self.set_xy(150, 12)
        self.cell(50, 10, "PATHOLOGY REPORT", 0, 0, 'R')
        self.ln(25)

    def footer(self):
        self.set_y(-25)
        # Line
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        
        # Disclaimer
        self.set_font('Arial', 'I', 7)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 4, "DISCLAIMER: This report is generated by an Artificial Intelligence system (YOLOv8) and is intended for preliminary screening purposes only. It does not constitute a final veterinary diagnosis. Please consult a licensed veterinarian for confirmation and prescription of medication.", align='C')
        
        # Page Number
        self.set_y(-15)
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'R')

def create_pdf(img_path, diagnosis, confidence, info):
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- SECTION 1: CASE INFORMATION (Grid Layout) ---
    pdf.set_font('Arial', 'B', 10)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_draw_color(200, 200, 200)
    
    # Row 1
    pdf.cell(30, 8, "Case ID:", 1, 0, 'L', 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(65, 8, f"TK-{random.randint(10000,99999)}", 1, 0, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 8, "Date:", 1, 0, 'L', 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(65, 8, datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 1, 1, 'L')
    
    # Row 2
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 8, "Specimen:", 1, 0, 'L', 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(65, 8, "Digital Skin Imaging (Porcine)", 1, 0, 'L')
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(30, 8, "Method:", 1, 0, 'L', 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(65, 8, "Computer Vision (YOLOv8)", 1, 1, 'L')
    pdf.ln(8)
    
    # --- SECTION 2: VISUAL FINDINGS ---
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "1. VISUAL FINDINGS", 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Image (Centered and Framed)
    try:
        x_pos = 55 # Center mostly
        pdf.image(img_path, x=x_pos, w=100)
        pdf.rect(x_pos, pdf.get_y() - (100 * 0.75), 100, (100 * 0.75)) # Border around image
        pdf.ln(5)
    except:
        pdf.cell(0, 10, "[Image Capture Error]", 0, 1)

    # --- SECTION 3: DIAGNOSTIC ASSESSMENT ---
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "2. DIAGNOSTIC ASSESSMENT", 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Result Table
    pdf.set_fill_color(245, 245, 245)
    
    # Header
    pdf.set_font('Arial', 'B', 10)
    pdf.set_text_color(0)
    pdf.cell(95, 8, "PRIMARY DETECTION", 1, 0, 'C', 1)
    pdf.cell(45, 8, "CONFIDENCE", 1, 0, 'C', 1)
    pdf.cell(50, 8, "SEVERITY", 1, 1, 'C', 1)
    
    # Data
    pdf.set_font('Arial', '', 10)
    pdf.cell(95, 10, clean_text(diagnosis.upper()), 1, 0, 'C')
    pdf.cell(45, 10, f"{confidence:.1f}%", 1, 0, 'C')
    
    # Severity Color/Text
    severity_txt = clean_text(info['severity'])
    pdf.cell(50, 10, severity_txt[:25], 1, 1, 'C')
    pdf.ln(8)
    
    # --- SECTION 4: PROTOCOL ---
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(0, 10, "3. RECOMMENDED PROTOCOL", 0, 1, 'L')
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 8, "Clinical Etiology:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, clean_text(info['cause']))
    pdf.ln(3)
    
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 8, "Treatment Plan:", 0, 1)
    pdf.set_font('Arial', '', 10)
    for step in info['steps']:
        pdf.cell(5) # Indent
        pdf.cell(0, 6, f"- {clean_text(step)}", 0, 1)
        
    pdf.ln(3)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 8, "Required Materials:", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, clean_text(info['materials']))

    # --- SIGNATURE BLOCK ---
    pdf.ln(20)
    pdf.set_draw_color(0)
    pdf.line(130, pdf.get_y(), 200, pdf.get_y()) # Line for signature
    pdf.set_xy(130, pdf.get_y() + 2)
    pdf.set_font('Arial', 'B', 9)
    pdf.cell(70, 5, "VERIFIED BY (VETERINARIAN)", 0, 1, 'C')
    pdf.set_font('Arial', '', 8)
    pdf.set_xy(130, pdf.get_y())
    pdf.cell(70, 5, "Signature over Printed Name / License No.", 0, 1, 'C')

    return pdf.output(dest='S').encode('latin-1')

# --- 5. REPORT GENERATOR HELPER ---
def generate_smart_report(detected_class, count, confidence):
    intros = [
        f"Analysis of the uploaded specimen indicates the presence of <b>{count} distinct anomaly/anomalies</b>.",
        f"The TUKLAS diagnostic system has flagged <b>{count} region(s) of interest</b> in this sample.",
    ]
    if "Healthy" in detected_class:
        return (f"Analysis complete. The system detected <b>{count} region(s)</b> classified as "
                f"<b>Healthy Skin</b>. With a confidence of <b>{confidence:.1f}%</b>, the animal "
                "appears free of visible pathologies.")
    return f"{random.choice(intros)} The morphological features are highly consistent with <b>{detected_class}</b> (Confidence: {confidence:.1f}%)."

# --- 6. CONTACTS DATA (Shortened for brevity in code block, logic remains) ---
contacts_data = [
    {"LGU": "Angono", "Office": "Municipal Veterinary Office", "Head": "Dr. Joel V. Tuplano", "Contact": "(02) 8451-1033", "Email": "officeofthemayor.angono@gmail.com"},
    {"LGU": "Antipolo City", "Office": "City Veterinary Office", "Head": "Dr. Rocelle D. Pico", "Contact": "(02) 8689-4514", "Email": "antipolocityvet@gmail.com"},
    {"LGU": "Baras", "Office": "Municipal Agriculture Office", "Head": "Mr. Jonathan Argueza", "Contact": "0920-958-1068", "Email": "lgubarasrizal@gmail.com"},
    {"LGU": "Binangonan", "Office": "Municipal Agriculture Office", "Head": "Department Head", "Contact": "(02) 8234-2124", "Email": "agriculture@binangonan.gov.ph"},
    {"LGU": "Tanay", "Office": "Municipal Agriculture Office", "Head": "Mr. Romeo B. Cruz", "Contact": "(02) 8655-1773", "Email": "tanay.agri@gmail.com"},
    # ... (Other contacts are safe to keep if you have them in your file)
]

# --- 7. CSS STYLING ---
st.markdown("""
    <style>
    .stApp { }
    .stButton>button {
        width: 100%;
        background-color: #1e3a8a; /* Navy Blue for Professional Look */
        color: white;
        font-weight: bold;
        border-radius: 5px;
        height: 3em;
        border: none;
    }
    .purple-box, .blue-box, .red-box, .yellow-box, .green-box {
        padding: 15px; border-radius: 4px; margin-bottom: 10px; border-left: 5px solid;
    }
    .purple-box { background: #f3e8ff; border-color: #6b21a8; color: #3b0764; }
    .blue-box { background: #eff6ff; border-color: #1e40af; color: #1e3a8a; }
    .red-box { background: #fef2f2; border-color: #b91c1c; color: #7f1d1d; }
    .yellow-box { background: #fefce8; border-color: #a16207; color: #713f12; }
    .green-box { background: #f0fdf4; border-color: #15803d; color: #14532d; }
    
    .report-box {
        background-color: white; color: #333; padding: 20px; 
        border: 1px solid #ddd; border-top: 5px solid #1e3a8a;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
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
    if lottie_microscope: st_lottie(lottie_microscope, height=150)
    st.title("TUKLAS Diagnostics")
    st.caption("Official Research Tool | RiSci")
    st.markdown("---")
    selected_page = st.selectbox("System Module", ["Lesion Analysis", "Local Directory"])
    
    if selected_page == "Lesion Analysis":
        conf_threshold = st.slider("AI Sensitivity", 0.0, 1.0, 0.40, 0.05)

# --- 10. MAIN APP LOGIC ---
if selected_page == "Lesion Analysis":
    st.title("🔬 Specimen Analysis Interface")
    st.markdown("Use this module to screen porcine skin samples for common pathologies.")
    
    uploaded_file = st.file_uploader("Upload Specimen Image", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        with open("temp_analysis.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())

        col1, col2 = st.columns([1, 1])
        with col1:
            st.image(img, use_container_width=True, caption="Source Image")

        if st.button("Initialize Analysis"):
            if model is None: st.error("Model missing.")
            else:
                with st.spinner("Processing image via YOLOv8..."):
                    with col2:
                        if lottie_scanning: st_lottie(lottie_scanning, height=100)
                    
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
                    st.image(result_plot, use_container_width=True, caption="Inference Result")

                st.divider()
                if count == 0:
                    st_green("✅ No pathologies detected within current sensitivity threshold.")
                else:
                    det_class = unique_detections[0] 
                    report_text = generate_smart_report(det_class, count, confidence)
                    
                    # Fetch Info
                    info = medical_data.get(det_class)
                    if not info:
                         for k in medical_data.keys():
                            if k in det_class or det_class in k:
                                info = medical_data[k]
                                break

                    # REPORT DISPLAY
                    with st.expander("📄 VIEW PRELIMINARY REPORT", expanded=True):
                        st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
                        if info:
                            pdf_bytes = create_pdf("temp_analysis.jpg", det_class, confidence, info)
                            st.download_button(
                                label="📥 Download Official Lab Report (PDF)",
                                data=pdf_bytes,
                                file_name=f"TUKLAS_Case_{int(time.time())}.pdf",
                                mime="application/pdf"
                            )

                    # PROTOCOLS
                    if info:
                        st.subheader("📋 Clinical Protocols")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Etiology & Transmission**")
                            st_blue(info['cause'])
                            st.markdown("**Required Materials**")
                            st_yellow(info['materials'])
                        with c2:
                            st.markdown("**Clinical Impact**")
                            st_red(info['harm'])
                            st.markdown("**Treatment Steps**")
                            step_txt = "\n".join([f"- {s}" for s in info['steps']])
                            st_green(step_txt)

elif selected_page == "Local Directory":
    st.title("📞 Municipal Directory")
    search_term = st.text_input("Filter by Municipality", "")
    
    visible = [c for c in contacts_data if search_term.lower() in c['LGU'].lower() or search_term == ""]
    if not visible: st.warning("No records found.")
    
    for data in visible:
        with st.expander(f"📍 {data['LGU']}"):
            st.write(f"**Office:** {data['Office']}")
            st.write(f"**Contact:** {data['Contact']}")

# Footer
st.markdown("---")
st.markdown("<center><small>System v1.0 | Rizal National Science High School Research</small></center>", unsafe_allow_html=True)
