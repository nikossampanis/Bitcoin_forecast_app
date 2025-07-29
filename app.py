import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Bitcoin Difficulty Forecast")

# --- HEADER WITH STYLE ---
st.markdown("""
<h1 style='text-align: center; color: #0072C6;'>📡 Bitcoin Difficulty Forecast</h1>
<h4 style='text-align: center;'>Developed by <span style='color:#FF914D;'>Gerasimos Dimitropoulos</span></h4>
<hr style='border: 1px solid #ccc;'>
""", unsafe_allow_html=True)

# --- LOAD EXCEL ---
try:
    df = pd.read_excel("bitcoin@public.xlsx")
    st.success("✅ Successfully loaded bitcoin@public.xlsx")
except Exception as e:
    st.error(f"❌ Could not load file: {e}")
    st.stop()

# --- CLEANING ---
df.rename(columns={"Date": "date"}, inplace=True)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date', 'DiffLast', 'HashRate', 'BlkCnt'])
df = df.sort_values("date")

# --- PREVIEW ---
st.markdown("### 📋 Dataset Preview")
st.dataframe(df[['date', 'DiffLast', 'HashRate', 'BlkCnt']].tail())

# --- LINE CHART ---
st.markdown("### 📈 Bitcoin Difficulty Over Time")
st.line_chart(df.set_index("date")["DiffLast"])

# --- SCATTER PLOT ---
st.markdown("### 🔄 HashRate vs Difficulty")
fig, ax = plt.subplots()
ax.scatter(df['HashRate'], df['DiffLast'], alpha=0.5, color='purple')
ax.set_xlabel("HashRate")
ax.set_ylabel("Difficulty")
st.pyplot(fig)

# --- REGRESSION & FORECAST ---
st.markdown("### 📊 Forecasting & Simulation")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔮 Linear Regression Forecast")
    df['days'] = (df['date'] - df['date'].min()).dt.days
    X = df[['days']]
    y = df['DiffLast']
    model = LinearRegression().fit(X, y)
    pred = model.predict(X)

    fig2, ax2 = plt.subplots()
    ax2.plot(df['date'], y, label="Actual", color="blue")
    ax2.plot(df['date'], pred, label="Forecast", linestyle="--", color="orange")
    ax2.set_title("Difficulty Forecast")
    ax2.set_ylabel("Difficulty")
    ax2.set_xlabel("Date")
    ax2.legend()
    st.pyplot(fig2)

with col2:
    st.subheader("🧪 What-if: Increase HashRate")
    factor = st.slider("Increase HashRate by (%)", 0, 200, 20)
    sim_difficulty = df['DiffLast'].iloc[-1] * (1 + factor / 100)
    st.success(f"📌 If HashRate increases by {factor}%, predicted difficulty: **{sim_difficulty:,.2f}**")

# --- MANUAL HASHRATE OVERRIDE ---
st.markdown("### ⚙️ Manual HashRate Override")
col3, col4 = st.columns(2)
current_hashrate = df['HashRate'].iloc[-1]

with col3:
    custom_hashrate = st.number_input("Set custom HashRate (same units as dataset):",
                                      min_value=0.0,
                                      value=float(current_hashrate),
                                      step=100.0)

with col4:
    if custom_hashrate > 0:
        custom_difficulty = df['DiffLast'].iloc[-1] * (custom_hashrate / current_hashrate)
        st.info(f"🟦 Projected Difficulty: **{custom_difficulty:,.2f}** for HashRate = {custom_hashrate:,.2f}")
