import streamlit as st
from PIL import Image
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="TUKLAS", page_icon="🐷")
st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# --- DEBUG INFO (To help us if it fails) ---
import sys
try:
    import ultralytics
    from ultralytics import YOLO
    st.success("✅ AI Brain (Ultralytics) is installed!")
except ImportError as e:
    st.error(f"❌ Critical Error: The 'ultralytics' library is missing.")
    st.info("Please check your 'requirements.txt' file on GitHub.")
    st.stop()

# --- PATH SETUP ---
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

# --- MODEL LOADING ---
if not os.path.exists(model_path):
    st.error(f"❌ Error: Cannot find 'best.pt' in {folder}")
else:
    @st.cache_resource
    def load_model():
        return YOLO(model_path)

    try:
        with st.spinner("Starting AI Engine..."):
            model = load_model()
        
        # --- UPLOAD & DETECT ---
        file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if file:
            img = Image.open(file)
            st.image(img, caption="Original", width=300)
            
            if st.button("🔍 Scan Image"):
                results = model(img)
                res_plotted = results[0].plot()
                st.image(res_plotted, caption="Detection Result")
                
    except Exception as e:
        st.error(f"Runtime Error: {e}")
