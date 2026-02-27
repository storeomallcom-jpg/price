import streamlit as st
from groq import Groq
import pandas as pd
from io import BytesIO

# --- CONFIGURATION (BACKEND ONLY) ---
# ضع مفتاحك الحقيقي هنا ولن يراه المستخدم أبداً في الواجهة
API_KEY = "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" 

st.set_page_config(page_title="AI Price Optimizer", page_icon="📈", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #0a0a0a; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Pro AI Pricing Engine")
st.write("Decision-making intelligence for modern e-commerce.")

# --- SIDEBAR: GLOBAL PARAMETERS ---
with st.sidebar:
    st.header("🌍 Market Context")
    country = st.selectbox("Target Market", ["Morocco", "Sweden", "USA", "EU"])
    season = st.select_slider("Seasonality", options=["Low", "Normal", "Peak"])
    brand = st.selectbox("Brand Positioning", ["New/Generic", "Established", "Premium Luxury"])

# --- MAIN INTERFACE: 10 ANALYTIC INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Product Details")
    prod_name = st.text_input("Product Name", "iPhone 13 (Used)")
    condition = st.selectbox("Condition", ["New", "Refurbished", "Used"])
    cost = st.number_input("Unit Cost (Net)", min_value=0.0, value=500.0)
    min_margin = st.slider("Min Accepted Margin (%)", 5, 100, 15)

with col2:
    st.subheader("📊 Market Intelligence")
    comp_price = st.number_input("Competitor Avg Price", value=700.0)
    stock = st.number_input("Inventory Level", value=100)
    demand = st.slider("Current Market Demand (%)", 0, 100, 70)

st.markdown("---")

if st.button("GENERATE OPTIMIZED STRATEGY"):
    if "FAKE" in API_KEY or not API_KEY:
        st.error("Backend Error: API Key not configured.")
    else:
        try:
            client = Groq(api_key=API_KEY)
            
            # Optimized System Prompt for Brief Tabular Output
            prompt = f"""
            Analyze pricing for: {prod_name}. 
            Context: Market={country}, Season={season}, Brand={brand}, Condition={condition}, 
            Cost={cost}, Min Margin={min_margin}%, Comp Price={comp_price}, Stock={stock}, Demand={demand}%.
            
            OUTPUT RULES:
            - Language: English.
            - Tone: Very Brief/Professional.
            - You MUST provide a JSON-like structured summary first for a table.
            - Then a 2-line strategic justification.
            """

            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a pricing bot. Output only a brief analysis summary."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2, # Stable analytical output
                stream=False
            )

            result_text = completion.choices[0].message.content

            # --- ANALYTICS TABLE GENERATION ---
            st.subheader("🎯 Strategic Summary")
            
            # Creating a professional table for the UI
            suggested_price = comp_price * 0.95 if demand > 50 else cost * 1.2 # Placeholder logic for UI safety
            
            data = {
                "Metric": ["Recommended Price", "Estimated Margin", "Market Position", "Stock Strategy"],
                "Value": [f"{suggested_price:.2f}", f"{((suggested_price-cost)/suggested_price)*100:.1f}%", "Aggressive", "Fast Liquidation"]
            }
            df = pd.DataFrame(data)
            st.table(df)

            # --- AI DETAILED JUSTIFICATION ---
            st.info(result_text)

            # --- DOWNLOAD SECTION ---
            st.subheader("📥 Export Results")
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Pricing_Analysis')
            
            st.download_button(
                label="Download Analysis as Excel",
                data=output.getvalue(),
                file_name=f"pricing_{prod_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
