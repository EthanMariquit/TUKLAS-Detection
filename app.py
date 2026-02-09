# --- 9. SIDEBAR ---
with st.sidebar:
    # Top Branding Area
    cols = st.columns([1, 4])
    with cols[0]:
        # The Logo (always visible)
        if lottie_microscope:
            st_lottie(lottie_microscope, height=60, key="sidebar_logo")
        else:
            st.image("https://img.icons8.com/fluency/96/microscope.png", width=50)
    
    with cols[1]:
        # The Text (Wrapped in a div that CSS can hide)
        st.markdown("""
            <div class="sidebar-text-container">
                <b style="font-size: 1.2rem;">TUKLAS Diagnostics</b><br>
                <small style="opacity: 0.7;">Veterinary Skin Lesion Analysis System</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    selected_page = st.selectbox("Navigate", ["🔍 Lesion Scanner", "📞 Local Directory"])
    
    st.markdown("---")
    st.subheader("💊 Rx Dosage Calculator")
    st.caption("Calculate injection volume based on body weight.")
    
    calc_weight = st.number_input("Pig Weight (kg)", min_value=1.0, value=50.0, step=0.5)
    drug_options = ["Select Drug..."] + [v['drug_name'] for k, v in medical_data.items() if 'drug_name' in v]
    selected_drug = st.selectbox("Medication", drug_options)
    
    if selected_drug != "Select Drug...":
        drug_info = next((v for k, v in medical_data.items() if v.get('drug_name') == selected_drug), None)
        if drug_info:
            vol = (calc_weight / drug_info['dosage_per_kg']) * drug_info['dosage_rate']
            st.info(f"**Administer:** {vol:.2f} mL")
            st.caption(f"Dosage Rate: {drug_info['dosage_rate']}mL per {drug_info['dosage_per_kg']}kg")
    
    st.markdown("---")
    conf_threshold = 0.25
    if selected_page == "🔍 Lesion Scanner":
        st.write("⚙️ **Scanner Settings**")
        conf_threshold = st.slider("Sensitivity", 0.0, 1.0, 0.40, 0.05)
        
        # --- RESTORED & AUTO-EXPANDED GUIDE ---
        st.markdown("---")
        with st.expander("📖 Quick Guide", expanded=True):
            st.write("1. **Upload** a clear photo of the skin lesion.")
            st.write("2. **Adjust** sensitivity if detection is too weak/strong.")
            st.write("3. **Review** the AI analysis and generated report.")
            st.write("4. **Consult** a licensed vet for final diagnosis.")
