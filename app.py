import streamlit as st
from PIL import Image
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="TUKLAS", page_icon="🐷")
st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# --- DEBUG & IMPORT ---
# We wrap the import in a try-block to catch the error gracefully
try:
    import ultralytics
    from ultralytics import YOLO
except ImportError:
    st.error("❌ System Error: The AI Brain (Ultralytics) failed to install.")
    st.info("Check the 'Manage App' logs to see if the installation ran out of memory.")
    st.stop()

# --- PATH SETUP ---
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

# --- MAIN APP ---
if not os.path.exists(model_path):
    st.error(f"❌ Error: 'best.pt' is missing. Found files: {os.listdir(folder)}")
else:
    @st.cache_resource
    def load_model():
        return YOLO(model_path)

    with st.spinner("Starting AI System..."):
        model = load_model()
    
    st.success("✅ TUKLAS Online")

    file = st.file_uploader("Upload Pig Image", type=['jpg', 'png', 'jpeg'])
    
    if file:
        img = Image.open(file)
        st.image(img, caption="Original Photo", width=300)
        
        if st.button("🔍 Analyze"):
            results = model(img)
            res_plotted = results[0].plot()
            st.image(res_plotted, caption="Detection Result")
