import os
import sys
import subprocess
import streamlit as st
from PIL import Image

# --- 1. SMART EMERGENCY INSTALL BLOCK ---
# We try to import. If it fails, we install the "Lite" version manually.
try:
    import ultralytics
    from ultralytics import YOLO
except ImportError:
    st.warning("⚙️ Installing AI Brain (First run only)...")
    
    # 1. Install CPU-only Torch (Prevents the heavy Nvidia download & Permission Error)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "torchvision", "--index-url", "https://download.pytorch.org/whl/cpu"])
    
    # 2. Install Ultralytics
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    
    # 3. Import again now that it's installed
    import ultralytics
    from ultralytics import YOLO

# ----------------------------------

# --- 2. PATH SETUP ---
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# --- 3. MODEL LOADING ---
if not os.path.exists(model_path):
    st.error(f"❌ FATAL ERROR: I cannot find 'best.pt'. \n\nI am looking in: {folder}")
    st.info("💡 TIP: Make sure 'best.pt' is in the SAME folder as 'app.py' on GitHub!")
else:
    @st.cache_resource
    def load_my_model():
        return YOLO(model_path)
    
    # Spinner for feedback
    with st.spinner("Loading AI Brain... (This might take a minute)"):
        model = load_my_model()
    
    st.success("✅ TUKLAS System is Online!")

    # --- 4. IMAGE UPLOAD ---
    file = st.file_uploader("Upload Pig Image", type=['jpg', 'png', 'jpeg'])

    if file:
        img = Image.open(file)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(img, caption="Original Photo", use_container_width=True)
        
        if st.button("🔍 Detect Lesions", type="primary"):
            with st.spinner("Scanning for lesions..."):
                results = model(img)
                res_plotted = results[0].plot()
                
                with col2:
                    st.image(res_plotted, caption="AI Detection Result", use_container_width=True)
                    
            count = len(results[0].boxes)
            if count > 0:
                st.warning(f"⚠️ Detected {count} potential lesions.")
            else:
                st.balloons()
                st.success("✅ No lesions detected!")
