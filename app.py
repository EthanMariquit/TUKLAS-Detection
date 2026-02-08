import streamlit as st
from PIL import Image
import os
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="TUKLAS Professional",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. MEDICAL KNOWLEDGE BASE (Updated with your 3 Classes) ---
# I am using the EXACT names you gave me. 
# If the AI fails to find them, we will see the "detected name" on screen to fix it.
medical_data = {
    "Diamond-shaped Plaques (Erysipelas)": {
        "severity": "High (Acute)",
        "cause": "Erysipelothrix rhusiopathiae bacteria. Often caused by sudden diet changes or contaminated soil.",
        "harm": "Can cause high fever, septicemia (blood poisoning), and sudden death if untreated.",
        "steps": [
            "Administer Penicillin (drug of choice) immediately.",
            "Isolate the sick pig from the herd.",
            "Disinfect pens with phenols or alkalis."
        ]
    },
    "Hyperkeratosis / Crusting (Sarcoptic Mange)": {
        "severity": "Moderate (Chronic)",
        "cause": "Sarcoptes scabiei var. suis (Mites). Spread by direct contact with infected pigs.",
        "harm": "Severe itching leads to weight loss, slow growth, and secondary infections from scratching.",
        "steps": [
            "Apply Ivermectin or Doramectin (injectable or feed additive).",
            "Spray sow herds with amitraz solutions.",
            "Treat all in-contact pigs, not just the visible ones."
        ]
    },
    "Greasy / Exudative Skin (Greasy Pig Disease)": {
        "severity": "High (in Piglets)",
        "cause": "Staphylococcus hyicus bacteria. Enters through bite wounds or abrasive floors.",
        "harm": "Causes dehydration and death in piglets; skin becomes greasy/oily and foul-smelling.",
        "steps": [
            "Wash pig with mild antiseptic soap and dry thoroughly.",
            "Administer antibiotics (Amoxicillin or Lincomycin).",
            "Clip 'needle teeth' in piglets to prevent facial biting."
        ]
    },
    "Healthy": { # Added just in case
        "severity": "None",
        "cause": "N/A",
        "harm": "N/A",
        "steps": ["Routine vaccination.", "Maintain hygiene."]
    }
}

# --- 3. THE "CREATIVE" REPORT WRITER ---
def generate_smart_report(detected_class, count, confidence):
    # Templates for the Intro
    intros = [
        f"Analysis of the uploaded specimen reveals **{count} distinct region(s)** of concern.",
        f"The TUKLAS diagnostic system has flagged **{count} potential anomaly/anomalies** in this sample.",
        f"Based on visual dermatological patterns, we identified **{count} area(s)** matching known pathology."
    ]
    
    # Templates for the Description
    descriptions = [
        f"The visual indicators are highly consistent with **{detected_class}**.",
        f"The AI has classified the skin texture and discoloration as **{detected_class}**.",
        f"Morphological features suggest the presence of **{detected_class}**."
    ]
    
    # Templates for the Confidence/Action
    actions = [
        f"With a confidence score of **{confidence:.1f}%**, immediate veterinary assessment is recommended.",
        f"The system is **{confidence:.1f}%** certain of this diagnosis. Please refer to the treatment protocols below.",
        f"Given the high confidence (**{confidence:.1f}%**), isolation protocols should be considered immediately."
    ]
    
    # Randomly pick one from each to make a unique paragraph
    text = f"{random.choice(intros)} {random.choice(descriptions)} {random.choice(actions)}"
    return text

# --- 4. CONTACTS DATA ---
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

# --- 5. CSS STYLING (Fixed White Text Issue) ---
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
    }
    /* Fixed the White Text Issue here */
    .report-box {
        background-color: #ffffff;
        color: #333333; /* Forces dark gray text */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        border-left: 5px solid #0056b3;
        font-family: 'Arial', sans-serif;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        z-index: 100;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 6. MODEL LOADING ---
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

# --- 7. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
    st.title("TUKLAS Diagnostics")
    st.caption("Veterinary Skin Lesion Analysis System")
    st.markdown("---")
    
    selected_page = st.selectbox("Navigate", ["🔍 Lesion Scanner", "📞 Local Directory"])
    st.markdown("---")

    conf_threshold = 0.40
    if selected_page == "🔍 Lesion Scanner":
        st.write("⚙️ **Scanner Settings**")
        conf_threshold = st.slider("Sensitivity", 0.0, 1.0, 0.40, 0.05)
        st.info("ℹ️ **How to use**\n1. Upload pig skin image.\n2. AI scans for anomalies.\n3. Review automated medical report.")

# --- 8. PAGE: LESION SCANNER ---
if selected_page == "🔍 Lesion Scanner":
    st.title("🔬 TUKLAS: Smart Veterinary Assistant")
    st.write("Upload a sample image to generate a comprehensive diagnostic report.")

    uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Original Sample")
            st.image(img, use_column_width=True, caption="Uploaded Image")

        if st.button("🔍 Generate Diagnostic Report"):
            if model is None:
                st.error("Model file missing.")
            else:
                with st.spinner("Analyzing tissue patterns..."):
                    results = model.predict(img, conf=conf_threshold)
                    result_plot = results[0].plot()
                    
                    # Get detected classes
                    detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
                    unique_detections = list(set(detected_classes))
                    count = len(detected_classes)
                    
                    # Get Confidence (Average of first detection if exists)
                    confidence = 0.0
                    if len(results[0].boxes) > 0:
                        confidence = float(results[0].boxes.conf[0]) * 100

                with col2:
                    st.subheader("🛡️ AI Detection")
                    st.image(result_plot, use_column_width=True, caption=f"Identified {count} regions of interest")

                # --- DYNAMIC REPORT SECTION ---
                st.markdown("---")
                st.subheader("📋 Automated Veterinary Report")
                
                if count == 0:
                    st.success("✅ No skin lesions detected. The specimen appears healthy based on current sensitivity settings.")
                else:
                    # 1. Generate the Paragraph
                    primary_detection = unique_detections[0] # Take the first one found
                    
                    # If the AI detects a name that ISN'T in our dictionary, show it raw
                    # This helps you debug if the names don't match!
                    display_name = primary_detection
                    
                    report_text = generate_smart_report(display_name, count, confidence)
                    
                    # Display the Paragraph in the styled box
                    st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
                    st.write("") 

                    # 2. Show Specific Medical Advice
                    for det_class in unique_detections:
                        # Try to find the exact match in our dictionary
                        info = medical_data.get(det_class)
                        
                        # If not found, try a "fuzzy" match (e.g. finding "Erysipelas" inside the long string)
                        if not info:
                            for key in medical_data.keys():
                                if key in det_class or det_class in key:
                                    info = medical_data[key]
                                    break
                        
                        if info:
                            with st.expander(f"🔴 Issue Detected: {det_class.upper()} (Click for Advice)", expanded=True):
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown(f"**Severity:** {info['severity']}")
                                    st.markdown(f"**Potential Causes:**\n{info['cause']}")
                                    st.markdown(f"**Potential Harms:**\n{info['harm']}")
                                with c2:
                                    st.markdown("**⚠️ Recommended Actions:**")
                                    for step in info['steps']:
                                        st.markdown(f"- {step}")
                        else:
                            st.error(f"⚠️ Unrecognized Class: '{det_class}'. Please update the code to match this name exactly.")

# --- 9. PAGE: DIRECTORY ---
elif selected_page == "📞 Local Directory":
    st.title("📞 Agricultural Support Directory")
    st.markdown("Find your local Municipal Agriculture Office or Veterinary Office below.")
    
    search_term = st.text_input("🔍 Search Municipality (e.g., 'Tanay', 'Antipolo')", "")
    st.markdown("---")

    col1, col2 = st.columns(2)
    visible_contacts = [c for c in contacts_data if search_term.lower() in c['LGU'].lower() or search_term == ""]
    
    if len(visible_contacts) == 0:
        st.warning("No offices found matching your search.")
    
    for i, data in enumerate(visible_contacts):
        with col1 if i % 2 == 0 else col2:
            with st.expander(f"📍 **{data['LGU']}**", expanded=True):
                st.markdown(f"**🏢 Office:** {data['Office']}")
                st.markdown(f"**👤 Head:** {data['Head']}")
                st.markdown(f"**📞 Phone:** `{data['Contact']}`")
                st.markdown(f"**✉️ Email:** {data['Email']}")
                st.caption("Operating Hours: Mon-Fri, 8AM - 5PM")

# --- 10. FOOTER ---
st.markdown("""
<div class="footer">
    <p><strong>Rizal National Science High School (RiSci)</strong><br>
    📍 J.P. Rizal St., Batingan, Binangonan, Rizal<br>
    📞 (02) 8652-2197 | ✉️ rnshs.admin@deped.gov.ph<br>
    © 2025 Student Research Project | TUKLAS Team</p>
</div>
""", unsafe_allow_html=True)
