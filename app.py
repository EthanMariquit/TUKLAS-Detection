import streamlit as st
from PIL import Image
import os

# --- 1. PAGE CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="TUKLAS Analysis",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS STYLING (For a cleaner look) ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        height: 3em;
        border-radius: 10px;
    }
    h1 {
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. MODEL LOADING ---
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

try:
    import ultralytics
    from ultralytics import YOLO
except ImportError:
    st.error("❌ System Error: Libraries missing.")
    st.stop()

if not os.path.exists(model_path):
    st.error("❌ Model not found. Please upload best.pt")
    st.stop()

@st.cache_resource
def load_model():
    return YOLO(model_path)

# --- 4. SIDEBAR DASHBOARD ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/pig.png", width=80)
    st.title("TUKLAS Control")
    st.markdown("---")
    
    st.write("⚙️ **Settings**")
    conf_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.25, 0.05, 
        help="Higher values mean the AI is stricter about what it calls a lesion.")
    
    st.markdown("---")
    st.info("ℹ️ **Instructions**\n\n1. Upload a clear photo.\n2. Adjust threshold if needed.\n3. Click Analyze.")

# --- 5. MAIN AREA ---
st.title("🔬 TUKLAS: Skin Lesion Analysis")
st.markdown("### Intelligent Veterinary Diagnostics")
st.write("Upload a sample image to detect and classify skin conditions automatically.")

# File Uploader
uploaded_file = st.file_uploader("", type=['jpg', 'png', 'jpeg'])

if uploaded_file:
    # Load the image
    img = Image.open(uploaded_file)
    
    # Create Columns for Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Sample")
        st.image(img, use_column_width=True, caption="Source Image")

    with col2:
        st.subheader("Analysis")
        # Place a placeholder button or result
        if st.button("🔍 Run Analysis"):
            with st.spinner("Processing image through AI model..."):
                model = load_model()
                # Run inference with the slider's threshold
                results = model.predict(img, conf=conf_threshold)
                
                # Plot the results
                res_plotted = results[0].plot()
                
                # Show Result
                st.image(res_plotted, use_column_width=True, caption="AI Detection Result")
                
                # Show Metrics (Optional Count)
                count = len(results[0].boxes)
                if count > 0:
                    st.success(f"✅ Detection Complete: Found {count} potential issues.")
                else:
                    st.warning("No lesions detected at this confidence level.")
