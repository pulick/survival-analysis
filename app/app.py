import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

# ------------------------------------ 1. STYLING & UTILITIES ------------------------------------
def custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #0E1117; color: #FFFFFF; }
        h1, h2, h3, p { color: #FFFFFF !important; }
        .result-card {
            background-color: #1A1C24;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-top: 25px;
        }
        .high-risk-border { border-top: 8px solid #FF4B4B !important; }
        .low-risk-border { border-top: 8px solid #00D166 !important; }
        div.stButton > button {
            background-color: transparent !important;
            border: 2px solid #3E424B !important;
            color: #FFFFFF !important;
            width: 100%;
            height: 3em;
            font-weight: bold;
            border-radius: 8px;
        }
        div.stButton > button:hover {
            background-color: #1f77b4 !important;
            border-color: #1f77b4 !important;
            color: white !important;
        }
        .status-text { font-size: 24px; font-weight: bold; }
        .prob-text { font-size: 42px; color: #1f77b4; font-weight: 800; }
        hr { border-top: 1px solid #3E424B !important; }
        </style>
    """, unsafe_allow_html=True)

def auto_scroll():
    components.html("<script>window.parent.document.querySelector('.main').scrollTo({top: 600, behavior: 'smooth'});</script>", height=0)

# ------------------------------------ 2. CONFIGURATION ------------------------------------
# This is the "Filter List". Any column NOT in this list will be ignored.
REQUIRED_GENES = [
    'CD44', 'GSTP1', 'IFITM3', 'GPRC5A', 'SCGB1B2P', 'CRYBG1', 'IGHG3', 'DDR1', 
    'MT-RNR2', 'IGSF1', 'S100A7', 'RPL12', 'TNC', 'EFEMP1', 'PBX1', 
    'S100A11', 'CD81', 'S100A9', 'SPP1', 'FOS'
]

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "xgb_model.pkl")

@st.cache_resource
def load_xgb_model():
    return joblib.load(MODEL_PATH)

# ------------------------------------ 3. MAIN APP ------------------------------------
def main():
    custom_css()
    st.title("🧬 Cancer Survival Predictor")
    st.markdown("<p style='color: #888;'>Automated Genomic Filtering & Risk Assessment</p>", unsafe_allow_html=True)
    st.divider()

    try:
        model = load_xgb_model()
    except:
        st.error("⚠️ Error: model/xgb_model.pkl not found.")
        st.stop()

    st.subheader("📂 Upload Patient Data")
    uploaded_file = st.file_uploader("Upload CSV (Will auto-filter for 20-gene signature)", type=["csv"])

    if uploaded_file is not None:
        raw_data = pd.read_csv(uploaded_file)
        
        # --- SMART FILTERING LOGIC ---
        # Check if all 20 genes exist in the uploaded file
        missing_genes = [gene for gene in REQUIRED_GENES if gene not in raw_data.columns]
        
        if missing_genes:
            st.error(f"❌ Missing Genes: {', '.join(missing_genes)}. Please ensure your CSV contains these columns.")
        else:
            # Drop everything else and keep genes in the EXACT order the model expects
            filtered_data = raw_data[REQUIRED_GENES]
            st.success(f"✅ Data Ready. Found all 20 genes. Ignored {len(raw_data.columns) - 20} extra columns.")

            if st.button("🔍 Run Prediction"):
                # Prediction
                prob_event = model.predict_proba(filtered_data)[:, 1][0]
                survival_prob = (1 - prob_event) * 100
                risk_level = "HIGH" if prob_event >= 0.5 else "LOW"
                
                # UI Helpers
                card_style = "high-risk-border" if risk_level == "HIGH" else "low-risk-border"
                risk_color = "#FF4B4B" if risk_level == "HIGH" else "#00D166"

                # Results Card
                st.markdown(f"""
                    <div class="result-card {card_style}">
                        <p style="color: #888; margin-bottom: 5px;">Analysis Result</p>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <span class="status-text">Risk Level: </span>
                                <span class="status-text" style="color: {risk_color}">{risk_level}</span>
                            </div>
                            <div>
                                <span class="status-text">Survival Probability: </span>
                                <span class="prob-text">{survival_prob:.0f}%</span>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.write("")
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🔝 Top Factors")
                    importances = model.feature_importances_
                    feat_imp = pd.DataFrame({'Gene': REQUIRED_GENES, 'Imp': importances}).sort_values('Imp', ascending=False)
                    
                    for _, row in feat_imp.head(4).iterrows():
                        gene_val = filtered_data[row['Gene']].values[0]
                        direction = "↑" if gene_val > 0 else "↓"
                        st.markdown(f"- Gene **{row['Gene']}** <span style='color:#1f77b4'>{direction}</span>", unsafe_allow_html=True)

                with col2:
                    st.subheader("📊 Gene Contribution")
                    plt.style.use('dark_background')
                    fig, ax = plt.subplots(figsize=(6, 4))
                    top_5 = feat_imp.head(5)
                    ax.barh(top_5['Gene'], top_5['Imp'], color='#1f77b4')
                    ax.invert_yaxis()
                    ax.set_facecolor('#1A1C24')
                    fig.patch.set_facecolor('#1A1C24')
                    st.pyplot(fig)

                auto_scroll()

    else:
        st.info("💡 Tip: You can upload a full TCGA file. I will automatically extract the 20 genes needed.")

if __name__ == "__main__":
    main()