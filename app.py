import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os

# This forces the computer to find the exact folder path
folder = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(folder, "best.pt")

st.title("🐷 TUKLAS: Pig Skin Lesion Detection")

# We check if the file exists before even trying to load it
if not os.path.exists(model_path):
    st.error(f"FATAL ERROR: I cannot find 'best.pt' in this folder: {folder}")
else:
    # 1. Load Model
    @st.cache_resource
    def load_my_model():
        return YOLO(model_path)
    
    model = load_my_model()
    st.success("✅ TUKLAS System is Online!")

    # 2. Upload
    file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])

    if file:
        img = Image.open(file)
        st.image(img, caption="Original Photo", width=400)
        
        if st.button("🔍 Detect Lesions"):
            results = model(img)
            # This draws the boxes
            res_plotted = results[0].plot()
            st.image(res_plotted, caption="AI Detection Result", width=600)
            st.metric("Total Lesions Found", len(results[0].boxes))