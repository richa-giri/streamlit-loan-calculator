import math
import pandas as pd
import streamlit as st

# Page settings
st.set_page_config(page_title="Loan Calculator", page_icon="💸", layout="centered")
st.title("💸 Loan Calculator")

# --- User Inputs ---
col1, col2 = st.columns(2)
name = col1.text_input("Your Name", placeholder="Enter your name")
age = col2.number_input("Age", min_value=18, max_value=80, value=25)

loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=500000, step=10000)
deposit = st.number_input("Down Payment (₹)", min_value=0, value=50000, step=5000)
interest_rate = st.slider("Interest Rate (%)", 1.0, 24.0, 9.0, 0.1)
years = st.slider("Loan Duration (Years)", 1, 30, 5)

insurance = st.toggle("Include Insurance (₹500/month)?", value=False)
show_table = st.checkbox("Show Amortization Table", value=True)

# --- Calculations ---
P = max(loan_amount - deposit, 0)  # Principal
monthly_rate = interest_rate / 100 / 12
n = years * 12

if monthly_rate == 0:
    emi = P / n
else:
    emi = P * monthly_rate * (1 + monthly_rate) ** n / ((1 + monthly_rate) ** n - 1)

if insurance:
    emi += 500

# --- Build Amortization Schedule ---
balance = P
rows = []
for month in range(1, n + 1):
    interest = balance * monthly_rate
    principal = emi - interest
    balance -= principal
    if balance < 0: balance = 0
    rows.append({"Month": month,
                 "EMI": round(emi, 2),
                 "Interest": round(interest, 2),
                 "Principal": round(principal, 2),
                 "Balance": round(balance, 2)})
df = pd.DataFrame(rows)

# --- Output Summary ---
st.subheader("Summary")
st.write({
    "Name": name or "—",
    "Age": age,
    "Principal (₹)": int(P),
    "Monthly EMI (₹)": round(emi, 2),
    "Total Interest (₹)": round(df["Interest"].sum(), 2),
    "Total Payment (₹)": round(df["EMI"].sum(), 2)
})

# --- Charts ---
st.subheader("Charts")
st.line_chart(df.set_index("Month")[["Balance"]])
st.area_chart(df.set_index("Month")[["Principal", "Interest"]])

# --- Show Table ---
if show_table:
    st.subheader("Amortization Table")
    st.dataframe(df, use_container_width=True)
