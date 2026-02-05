import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# 1. Page Configuration
st.set_page_config(page_title="TUKLAS Pig Detection", layout="wide")
st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# 2. Path Setup (Finds the model in the same folder)
folder_path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder_path, "best.pt")

# 3. Model Loading Logic
if not os.path.exists(model_path):
    st.error(f"❌ Error: 'best.pt' not found in {folder_path}. Please check your GitHub files.")
else:
    @st.cache_resource
    def load_model():
        return YOLO(model_path)

    try:
        with st.spinner("Loading AI Brain..."):
            model = load_model()
        st.success("✅ TUKLAS System is Online!")

        # 4. Image Uploader
        uploaded_file = st.file_uploader("Upload Pig Photo", type=['jpg', 'png', 'jpeg'])

        if uploaded_file:
            col1, col2 = st.columns(2)
            
            # Open and display original image
            img = Image.open(uploaded_file)
            with col1:
                st.image(img, caption="Original Photo", use_container_width=True)

            # Detection Button
            if st.button("🔍 Run AI Detection", type="primary"):
                with st.spinner("Analyzing..."):
                    results = model(img)
                    res_plotted = results[0].plot()
                    
                    with col2:
                        st.image(res_plotted, caption="Detection Result", use_container_width=True)
                        
                    # Metrics
                    count = len(results[0].boxes)
                    if count > 0:
                        st.warning(f"⚠️ Found {count} lesion(s).")
                    else:
                        st.success("✅ No lesions detected.")

    except Exception as e:
        st.error(f"An error occurred while loading the model: {e}")

