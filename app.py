import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="TUKLAS Spy", layout="wide")
st.title("🕵️ TUKLAS System Spy")

st.write("Checking installed libraries...")

# 1. Ask the computer to list everything it has installed
try:
    # Run 'pip list' to get a full inventory
    result = subprocess.check_output([sys.executable, "-m", "pip", "list"], encoding='utf-8')
    
    # Display the result in a text box
    st.text_area("📦 INSTALLED PACKAGES:", result, height=400)
    
    # Check specifically for the ones we need
    required = ["ultralytics", "torch", "opencv-python", "opencv-python-headless"]
    st.subheader("🔍 Critical Check:")
    
    for lib in required:
        if lib in result:
            st.success(f"✅ {lib} is installed!")
        else:
            st.error(f"❌ {lib} is MISSING.")
            
except Exception as e:
    st.error(f"Spy failed: {e}")

# 2. Check where the computer is looking for files
st.subheader("📂 Current Folder:")
import os
st.code(os.getcwd())
st.write("Files here:", os.listdir("."))
