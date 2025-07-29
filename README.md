
# 📊 Bitcoin Difficulty Forecast App

This Streamlit application allows you to explore, visualize, and forecast the historical **Bitcoin network mining difficulty** using real data.

## ✅ Features
- 📈 Line chart showing difficulty over time
- 🔄 Scatter plot of HashRate vs Difficulty
- 🔮 Forecast of difficulty using linear regression over time
- 🧪 Interactive "What-if" simulation: estimate difficulty change if HashRate increases

## 📁 Input File
- `bitcoin@public.xlsx`: Excel file with columns:
  - `Date`: timestamp of the data
  - `DiffLast`: blockchain mining difficulty
  - `HashRate`: network hashrate
  - `BlkCnt`: number of blocks mined

## 🔢 Mathematical Concepts Required
To understand the visualizations, you should be familiar with:
- **Time Series Data**: plotting metrics over chronological time
- **Linear Regression**: using linear models to predict future values
- **Percent Change Calculations**: modeling "what-if" scenarios with formula D' = D × (1 + r)

## ▶️ How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

Place the `bitcoin@public.xlsx` in the same folder as the app.
