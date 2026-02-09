# --- 9. SIDEBAR OPTIMIZATION (Restored Typable & Compact Layout) ---
with st.sidebar:
    # 9.1 Brand Header (Compact & Centered)
    st.markdown("<div style='text-align: center; margin-top: -50px;'>", unsafe_allow_html=True)
    if lottie_microscope:
        st_lottie(lottie_microscope, height=100, key="sidebar_anim")
    else:
        st.markdown("### 🔬")
    
    st.markdown("<h2 style='margin-bottom: 0;'>TUKLAS</h2>", unsafe_allow_html=True)
    st.caption("Veterinary Skin Lesion Analysis")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 9.2 Navigation Section (Typable Selectbox Restored)
    with st.expander("🛠️ Main Navigation", expanded=True):
        selected_page = st.selectbox(
            "Go to:", 
            ["🔍 Lesion Scanner", "📞 Local Directory"],
            index=0,
            help="Type to search for a specific tool"
        )
        
        # Guide moved inside for a cleaner look
        st.markdown("<br>", unsafe_allow_html=True)
        st.write("**Quick Guide**")
        st.caption("• Upload lesion photo.")
        st.caption("• Adjust sensitivity.")
        st.caption("• Review AI report.")
    
    st.markdown("---")
    
    # 9.3 Calculator Section (Typable Drug Selection)
    st.subheader("💊 Rx Dosage Calculator")
    calc_weight = st.number_input("Pig Weight (kg)", min_value=1.0, value=50.0, step=0.5)
    
    # Restored Typable Medication Selection
    drug_options = ["Select Drug..."] + [v['drug_name'] for k, v in medical_data.items() if 'drug_name' in v]
    selected_drug = st.selectbox("Medication", drug_options)
    
    if selected_drug != "Select Drug...":
        drug_info = next((v for k, v in medical_data.items() if v.get('drug_name') == selected_drug), None)
        if drug_info:
            vol = (calc_weight / drug_info['dosage_per_kg']) * drug_info['dosage_rate']
            st.info(f"**Administer:** {vol:.2f} mL")
            st.caption(f"Rate: {drug_info['dosage_rate']}mL per {drug_info['dosage_per_kg']}kg")
    
    st.markdown("---")
    
    # 9.4 Scanner Settings
    if selected_page == "🔍 Lesion Scanner":
        st.write("⚙️ **Scanner Settings**")
        conf_threshold = st.slider("Sensitivity (Confidence)", 0.0, 1.0, 0.40, 0.05)
    else:
        conf_threshold = 0.25
