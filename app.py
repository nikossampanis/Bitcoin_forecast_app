
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Bitcoin Difficulty Forecast from Dataset")

st.markdown("**Developed by Gerasimos Dimitropoulos**")

# 🔹 Load local Excel
try:
    df = pd.read_excel("bitcoin@public.xlsx")
    st.success("✅ Loaded bitcoin@public.xlsx")
except Exception as e:
    st.error(f"❌ Could not load file: {e}")
    st.stop()

# 🧼 Clean & rename
df.rename(columns={"Date": "date"}, inplace=True)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date', 'DiffLast', 'HashRate', 'BlkCnt'])
df = df.sort_values("date")

# 🔍 Preview
st.subheader("📋 Dataset Preview")
st.dataframe(df[['date', 'DiffLast', 'HashRate', 'BlkCnt']].tail())

# 📈 Plot Difficulty Over Time
st.subheader("📈 Bitcoin Difficulty Over Time")
st.line_chart(df.set_index("date")["DiffLast"])

# 🔄 Scatter: HashRate vs Difficulty
st.subheader("🔄 HashRate vs Difficulty")
fig, ax = plt.subplots()
ax.scatter(df['HashRate'], df['DiffLast'], alpha=0.5)
ax.set_xlabel("HashRate")
ax.set_ylabel("Difficulty")
st.pyplot(fig)

# 🔮 Forecasting with Linear Regression
st.subheader("🔮 Forecasting Difficulty with Linear Regression")
df['days'] = (df['date'] - df['date'].min()).dt.days
X = df[['days']]
y = df['DiffLast']
model = LinearRegression().fit(X, y)
pred = model.predict(X)

fig2, ax2 = plt.subplots()
ax2.plot(df['date'], y, label="Actual", color="blue")
ax2.plot(df['date'], pred, label="Forecast", linestyle="--", color="orange")
ax2.set_title("Forecasting Bitcoin Difficulty")
ax2.set_ylabel("Difficulty")
ax2.set_xlabel("Date")
ax2.legend()
st.pyplot(fig2)

# 🧪 What-if Simulation
st.subheader("🧪 What-if Simulation: Increase HashRate")
factor = st.slider("Increase HashRate by (%)", 0, 200, 20)
sim_difficulty = df['DiffLast'].iloc[-1] * (1 + factor / 100)
st.markdown(f"""
📌 If the hashrate increases by **{factor}%**,  
the predicted difficulty would be:  
### 🟠 **{sim_difficulty:,.2f}**
""")

# ⚙️ Manual HashRate Override
st.subheader("⚙️ Manual HashRate Override")
current_hashrate = df['HashRate'].iloc[-1]
custom_hashrate = st.number_input("Set custom HashRate (same units as dataset):",
                                  min_value=0.0,
                                  value=float(current_hashrate),
                                  step=100.0)

if custom_hashrate > 0:
    projected_difficulty = df['DiffLast'].iloc[-1] * (custom_hashrate / current_hashrate)
    st.markdown(f"""
    🧮 Based on custom HashRate = **{custom_hashrate:,.2f}**,  
    projected difficulty is:  
    ### 🔵 **{projected_difficulty:,.2f}**
    """)
