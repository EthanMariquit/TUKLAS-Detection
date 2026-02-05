import os
import sys
import subprocess

# --- 1. EMERGENCY INSTALL BLOCK ---
# This forces the cloud to install the library if it's missing
try:
    import ultralytics
except ImportError:
    # If the computer says "Module Not Found", we run this command to install it right now
    subprocess.check_call([sys.executable, "-m", "pip", "install", "ultralytics"])
    import ultralytics
# ----------------------------------

import streamlit as st
from ultralytics import YOLO
from PIL import Image

# --- 2. PATH SETUP ---
# This finds the exact folder where this script is running
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
    
    # We add a spinner so you know it's working
    with st.spinner("Loading AI Brain... (This might take a minute)"):
        model = load_my_model()
    
    st.success("✅ TUKLAS System is Online!")

    # --- 4. IMAGE UPLOAD ---
    file = st.file_uploader("Upload Pig Image", type=['jpg', 'png', 'jpeg'])

    if file:
        img = Image.open(file)
        
        # Create two columns for a side-by-side view
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(img, caption="Original Photo", use_container_width=True)
        
        if st.button("🔍 Detect Lesions", type="primary"):
            with st.spinner("Scanning for lesions..."):
                results = model(img)
                res_plotted = results[0].plot()
                
                with col2:
                    st.image(res_plotted, caption="AI Detection Result", use_container_width=True)
                    
            # Count the boxes
            count = len(results[0].boxes)
            if count > 0:
                st.warning(f"⚠️ Detected {count} potential lesions.")
            else:
                st.balloons()
                st.success("✅ No lesions detected!")
