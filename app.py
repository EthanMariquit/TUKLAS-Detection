import streamlit as st
import os
import sys
import subprocess
import importlib.util

# --- 1. THE "NO-FAIL" INSTALLER ---
# This function uses only standard Python tools to check and install
def ensure_library(name, package_name=None):
    if package_name is None:
        package_name = name
        
    # Check if installed using standard 'importlib' (No pkg_resources needed)
    if importlib.util.find_spec(name) is None:
        st.warning(f"⚙️ Installing {name}... (This may take 2 minutes)")
        try:
            # Install to USER folder to avoid Permission Error
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--user", package_name, "--quiet"
            ])
            st.success(f"✅ {name} installed!")
        except Exception as e:
            st.error(f"❌ Failed to install {name}: {e}")
            st.stop()

# --- 2. RUN INSTALL CHECKS ---
# We force these checks before anything else loads
try:
    # 1. Install Streamlit (Just in case, though it should be there)
    ensure_library("streamlit")
    
    # 2. Install Ultralytics (The AI Brain)
    # We install specifically without dependencies first to avoid conflicts, then let it resolve
    ensure_library("ultralytics")
    
    # --- CRITICAL: ADD INSTALL FOLDER TO PATH ---
    # Since we installed with '--user', we must tell Python where to look
    import site
    import importlib
    
    # Reload site packages to find the new files
    importlib.reload(site)
    
except Exception as e:
    st.error(f"Setup Error: {e}")

# --- 3. THE ACTUAL APP CODE ---
# Now we can safely import everything
try:
    from ultralytics import YOLO
    from PIL import Image

    # Page Config
    st.set_page_config(page_title="TUKLAS", page_icon="🐷")
    st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

    # Path Setup
    folder = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(folder, "best.pt")

    # Load Model
    if not os.path.exists(model_path):
        st.error(f"❌ Error: Cannot find 'best.pt' in {folder}")
    else:
        @st.cache_resource
        def load_model():
            return YOLO(model_path)

        with st.spinner("Starting AI Engine..."):
            model = load_model()
        
        st.success("✅ System Online")

        # Upload
        file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if file:
            img = Image.open(file)
            st.image(img, caption="Original", width=300)
            
            if st.button("🔍 Scan Image"):
                results = model(img)
                res_plotted = results[0].plot()
                st.image(res_plotted
