import streamlit as st
import os
import sys
import subprocess
import pkg_resources

# --- PART 1: DIAGNOSTIC & STEALTH INSTALL ---
st.set_page_config(page_title="TUKLAS Debugger")
st.title("🛠️ TUKLAS: Diagnostics & Recovery")

# 1. Show us exactly what files exist in the cloud folder
st.subheader("📂 Cloud File Check")
files = os.listdir(".")
st.write("Files found in current folder:", files)

# Check specifically for requirements.txt errors
if "requirements.txt" in files:
    st.success("✅ 'requirements.txt' was found.")
elif "requirements.txt.txt" in files:
    st.error("❌ FOUND ERROR: File is named 'requirements.txt.txt'. Rename it on GitHub!")
else:
    st.warning("⚠️ 'requirements.txt' is MISSING from this folder.")

# 2. Force Install "User Mode" (Bypasses Permission Error)
try:
    import ultralytics
    st.success("✅ Ultralytics is already installed!")
except ImportError:
    st.warning("⚙️ Ultralytics missing. Attempting Stealth Install...")
    try:
        # The flag '--user' installs it in a folder we are ALLOWED to write to
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--user", "ultralytics", "--no-warn-script-location"
        ])
        
        # We must tell Python where the new 'user' folder is
        # Add the local user site-packages to the path
        user_site = subprocess.check_output([sys.executable, "-m", "site", "--user-site"]).decode().strip()
        if user_site not in sys.path:
            sys.path.append(user_site)
            
        import ultralytics
        st.success("🎉 Stealth Install SUCCESS! Reloading...")
        st.experimental_rerun()
        
    except Exception as e:
        st.error(f"❌ Install Failed: {e}")

# --- PART 2: THE ACTUAL APP ---
# Only run this if installation succeeded
if 'ultralytics' in sys.modules:
    from ultralytics import YOLO
    from PIL import Image

    folder = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(folder, "best.pt")

    if not os.path.exists(model_path):
        st.error(f"❌ 'best.pt' NOT FOUND. (Is it named 'best (3).pt'?)")
    else:
        # Load Model
        model = YOLO(model_path)
        
        st.markdown("---")
        st.header("🐷 Pig Lesion Detection")
        
        file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
        if file:
            img = Image.open(file)
            st.image(img, caption="Original", width=300)
            
            if st.button("Run Detection"):
                results = model(img)
                res_plotted = results[0].plot()
                st.image(res_plotted, caption="Result")
