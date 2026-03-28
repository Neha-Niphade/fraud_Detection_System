import streamlit as st
import mysql.connector
import pandas as pd
import requests
import plotly.graph_objects as go
import os

# ---------------- DB CONNECTION ----------------
# Wrapped in try-except to prevent crash if DB is not running
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "kk02"),
        database=os.getenv("DB_NAME", "fraud_db")
    )
    cursor = db.cursor()
except Exception as e:
    st.error(f"Database Connection Error: {e}")

# Professional setup
st.set_page_config(
    page_title="Fraud Sentinel AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN CONSOLIDATED CSS ---
st.markdown("""
    <style>
        /* Main Background */
        .main { background-color: #0e1117; color: #ffffff; }
        
        /* Neon Glow Button */
        .stButton>button {
            background: linear-gradient(45deg, #00d4ff, #00ffaa) !important;
            color: #0e1117 !important;
            font-weight: 800 !important;
            border: none !important;
            padding: 12px 40px !important;
            border-radius: 30px !important;
            box-shadow: 0 0 15px rgba(0, 212, 255, 0.4) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            width: 100%;
        }
        .stButton>button:hover {
            box-shadow: 0 0 25px rgba(0, 255, 170, 0.6) !important;
            transform: scale(1.02) !important;
        }

        /* Glassmorphism Cards */
        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
            backdrop-filter: blur(10px);
        }

        /* Hide Sidebar Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
API_URL = os.getenv("API_URL", "http://127.0.0.1:5000")

with st.sidebar:
    st.header(" System Status")
    st.markdown("---")
    st.success("🛰️ API: Online")
    st.code(API_URL)
    st.markdown("---")
    st.info("Adjust parameters and execute neural analysis.")
    if st.button("🔄 Refresh System"):
        st.rerun()

# ---------------- HEADER ----------------
st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.03); padding: 40px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.1); text-align: center; margin-bottom: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
        <p style="color: #00d4ff; letter-spacing: 3px; text-transform: uppercase; font-size: 14px; font-weight: 600; margin-bottom: 10px;">Real-Time Neural Monitoring</p>
        <h1 style="font-family: 'Inter', sans-serif; font-size: 55px; font-weight: 800; background: linear-gradient(90deg, #00d4ff 0%, #00ffaa 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">🛡️ FRAUD SENTINEL</h1>
        <div style="width: 50px; height: 3px; background: #00d4ff; margin: 20px auto; border-radius: 10px;"></div>
    </div>
""", unsafe_allow_html=True)

# =========================
# 1️⃣ INPUT SECTION
# =========================
st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.02); padding: 20px; border-radius: 15px; border-left: 5px solid #00d4ff; margin-bottom: 20px;">
        <h3 style="color: #fff; margin: 0;"> Transaction Parameters</h3>
    </div>
""", unsafe_allow_html=True)

col_t1, col_t2 = st.columns(2)
with col_t1:
    time = st.number_input(" Time (Offset Seconds)", value=0.0, format="%.2f")
with col_t2:
    amount = st.number_input(" Transaction Amount ($)", value=0.0, format="%.2f")

with st.expander(" Neural Latent Features (V1 - V28)", expanded=False):
    features = []
    rows, cols_per_row = 4, 7
    for r in range(rows):
        st_cols = st.columns(cols_per_row)
        for c in range(cols_per_row):
            idx = r * cols_per_row + c + 1
            val = st_cols[c].number_input(f"V{idx}", value=0.0, format="%.2f", key=f"v{idx}")
            features.append(val)

if st.button(" Execute Fraud Scan"):
    try:
        input_data = [time] + features + [amount]
        response = requests.post(f"{API_URL}/predict", json={"features": input_data})
        data = response.json()
        
        res = data["prediction"]
        prob = data["probability"]

        if res == "Fraud":
            st.error(f" ALERT: FRAUD DETECTED ({prob*100:.2f}% Confidence)")
        else:
            st.success(f" CLEAR: SECURE TRANSACTION ({prob*100:.2f}% Risk)")
    except:
        st.warning(" Connection to Prediction API failed. Ensure Flask is running.")

st.markdown("---")

# =========================
# 2️⃣ ANALYTICS SECTION
# =========================
st.markdown("### Live Analytics Dashboard")
query = "SELECT * FROM transactions"
df = pd.read_sql(query, db)

total = len(df)
fraud = len(df[df['prediction'] == 'Fraud'])
rate = (fraud/total*100) if total > 0 else 0

# Custom Glass Metrics
st.markdown(f"""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
        <div class="metric-card">
            <p style="color: #888; margin: 0; font-size: 14px;">Total Processed</p>
            <h2 style="color: #fff; margin: 10px 0; font-size: 32px;">{total}</h2>
        </div>
        <div class="metric-card" style="border: 1px solid rgba(255, 75, 75, 0.2);">
            <p style="color: #ff4b4b; margin: 0; font-size: 14px;">Threats Blocked</p>
            <h2 style="color: #ff4b4b; margin: 10px 0; font-size: 32px;">{fraud}</h2>
        </div>
        <div class="metric-card" style="border: 1px solid rgba(0, 255, 170, 0.2);">
            <p style="color: #00ffaa; margin: 0; font-size: 14px;">Fraud Rate</p>
            <h2 style="color: #00ffaa; margin: 10px 0; font-size: 32px;">{rate:.2f}%</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

# Plotly Charts
col_c1, col_c2 = st.columns([2, 1])

with col_c1:
    st.markdown("#####  Fraud Trends")
    st.bar_chart(df['prediction'].value_counts())

with col_c2:
    st.markdown("#####  Composition")
    chart_data = df['prediction'].value_counts()
    fig = go.Figure(data=[go.Pie(labels=chart_data.index, values=chart_data.values, hole=.6)])
    fig.update_layout(
        showlegend=False, height=250, margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white"
    )
    fig.update_traces(marker=dict(colors=['#00ffaa', '#ff4b4b']))
    st.plotly_chart(fig, use_container_width=True)

# =========================
# 3️⃣ DATA RECORDS
# =========================
st.markdown("### Secure Transaction Logs")

# Visual Polish: Drop the messy feature list for the main table
display_df = df.drop(columns=['features']) if 'features' in df.columns else df

def style_rows(row):
    color = 'rgba(255, 75, 75, 0.15)' if row['prediction'] == 'Fraud' else 'transparent'
    return [f'background-color: {color}'] * len(row)

st.dataframe(
    display_df.style.apply(style_rows, axis=1),
    use_container_width=True,
    height=300
)

st.markdown("---")
st.caption("Fraud Sentinel v2.0 | Neural Encryption Active")