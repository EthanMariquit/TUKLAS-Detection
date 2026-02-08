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

# --- 2. THE MEDICAL KNOWLEDGE BASE ---
# These keys match the EXACT names your YOLO model was trained on.
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
    }
}

# --- 3. THE "CREATIVE" REPORT ENGINE (NLP) ---
def generate_smart_report(detected_class, count, confidence):
    # 1. The Opening (Sets the scene)
    intros = [
        f"Analysis of the uploaded specimen indicates the presence of **{count} distinct anomaly/anomalies**.",
        f"The TUKLAS diagnostic system has flagged **{count} region(s) of interest** in this sample.",
        f"Based on visual dermatological patterns, our AI identified **{count} area(s)** requiring attention.",
        f"A thorough scan of the tissue sample reveals **{count} point(s) of concern**."
    ]
    
    # 2. The Diagnosis (Identifies the issue)
    descriptions = [
        f"The morphological features are highly consistent with **{detected_class}**.",
        f"The AI has classified the skin texture and discoloration patterns as **{detected_class}**.",
        f"Visual indicators suggest a high probability of **{detected_class}**.",
        f"The detected lesions exhibit characteristics typical of **{detected_class}**."
    ]
    
    # 3. The Action/Confidence (What to do next)
    actions = [
        f"With a confidence score of **{confidence:.1f}%**, immediate veterinary assessment is recommended.",
        f"The system is **{confidence:.1f}%** certain of this diagnosis. Please refer to the treatment protocols below.",
        f"Given the high confidence (**{confidence:.1f}%**), isolation protocols should be initiated immediately.",
        f"The model's certainty is **{confidence:.1f}%**. We advise cross-referencing this with a physical exam."
    ]
    
    # Mix and match them randomly!
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

# --- 5. CSS STYLING (The "Professional Polish") ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #0056b3;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #004494;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    /* The Report Box - FORCED BLACK TEXT */
    .report-box {
        background-color: #ffffff;
        color: #333333; 
        padding: 25px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 6px solid #0056b3;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 16px;
        line-height: 1.6;
    }

    /* Contact Cards */
    .contact-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }

    /* Footer */
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

# --- 7. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
    st.title("TUKLAS Diagnostics")
    st.caption("Veterinary Skin Lesion Analysis System")
    st.markdown("---")
    
    selected_page = st.selectbox("Navigate", ["🔍 Lesion Scanner", "📞 Local Directory"])
    st.markdown("---")

    conf_threshold = 0.25 # Default
    if selected_page == "🔍 Lesion Scanner":
        st.write("⚙️ **Scanner Settings**")
        conf_threshold = st.slider("Sensitivity Threshold", 0.0, 1.0, 0.40, 0.05)
        st.info("ℹ️ **Usage Guide**\n1. Upload a clear image of the skin.\n2. The AI will highlight anomalies.\n3. Review the generated medical report.")

# --- 8. PAGE: LESION SCANNER ---
if selected_page == "🔍 Lesion Scanner":
    st.title("🔬 TUKLAS: Smart Veterinary Assistant")
    st.markdown("### Automated Detection & Diagnostics")
    st.write("Upload a sample image to generate a comprehensive diagnostic report.")

    uploaded_file = st.file_uploader("Upload Image (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

    if uploaded_file:
        img = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📸 Original Sample")
            st.image(img, use_column_width=True, caption="Uploaded Specimen")

        if st.button("🔍 Generate Diagnostic Report"):
            if model is None:
                st.error("Model file missing.")
            else:
                with st.spinner("Analyzing tissue patterns..."):
                    # Run the AI
                    results = model.predict(img, conf=conf_threshold)
                    result_plot = results[0].plot()
                    
                    # Extract Data
                    detected_classes = [model.names[int(box.cls)] for box in results[0].boxes]
                    unique_detections = list(set(detected_classes))
                    count = len(detected_classes)
                    
                    # Calculate Confidence (Average)
                    confidence = 0.0
                    if len(results[0].boxes) > 0:
                        confs = results[0].boxes.conf.tolist()
                        confidence = (sum(confs) / len(confs)) * 100

                with col2:
                    st.subheader("🛡️ AI Detection Results")
                    st.image(result_plot, use_column_width=True, caption=f"Identified {count} anomalies")
                    
                    # Show Confidence Meter (Visual Polish!)
                    if count > 0:
                        st.metric(label="AI Confidence Score", value=f"{confidence:.1f}%")
                        st.progress(int(confidence))

                # --- DYNAMIC REPORT SECTION ---
                st.markdown("---")
                st.subheader("📋 Automated Veterinary Report")
                
                if count == 0:
                    st.success("✅ **Negative Result:** No skin lesions detected based on current sensitivity settings. The specimen appears healthy.")
                else:
                    # 1. Generate the "Creative" Paragraph
                    # We pick the first detection to write the story about
                    primary_detection = unique_detections[0] 
                    report_text = generate_smart_report(primary_detection, count, confidence)
                    
                    # Display the styled box
                    st.markdown(f'<div class="report-box">{report_text}</div>', unsafe_allow_html=True)
                    st.write("") 

                    # 2. Show Medical Advice (Accordion Style)
                    for det_class in unique_detections:
                        # Match logic: Try exact match first
                        info = medical_data.get(det_class)
                        
                        # Fallback: Check if partial match (e.g., "Erysipelas" inside "Erysipelas (Diamond Skin)")
                        if not info:
                            for key in medical_data.keys():
                                if key in det_class or det_class in key:
                                    info = medical_data[key]
                                    break
                        
                        if info:
                            with st.expander(f"🔴 Issue Detected: {det_class} (Click for Protocol)", expanded=True):
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown(f"**Severity Level:**\n{info['severity']}")
                                    st.markdown(f"**Potential Causes:**\n{info['cause']}")
                                with c2:
                                    st.markdown(f"**Potential Harms:**\n{info['harm']}")
                                
                                st.markdown("---")
                                st.markdown("**⚠️ Recommended Actions:**")
                                for step in info['steps']:
                                    st.markdown(f"- {step}")
                        else:
                            st.warning(f"⚠️ **Note:** The class '{det_class}' was detected, but no specific medical protocol is currently loaded in the database.")

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
