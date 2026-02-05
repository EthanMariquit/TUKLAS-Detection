import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# 1. Page Setup
st.set_page_config(page_title="TUKLAS", layout="wide")
st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# 2. Path Setup
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

# 3. Load Model
if not os.path.exists(model_path):
    st.error(f"❌ Error: 'best.pt' not found in: {folder}")
else:
    @st.cache_resource
    def load_model():
        return YOLO(model_path)

    # Simple loading without the complex error handling blocks
    try:
        with st.spinner("Loading AI System..."):
            model = load_model()
        st.success("✅ System Online")
        
        # 4. Upload & Detect
        uploaded_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Image", width=300)
            
            if st.button("🔍 Analyze"):
                results = model(img)
                res_plotted = results[0].plot()
                st.image(res_plotted, caption="Result", width=500)
                
    except Exception as e:
        st.error(f"Error loading model: {e}")
