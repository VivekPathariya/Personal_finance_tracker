# Import required libraries
import streamlit as st
import pandas as pd
import os

#backgrund colour 
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Title
st.title("💰 Personal Finance Tracker")

# Sidebar Menu
menu = st.sidebar.selectbox("Select Option", ["Add Income", "Add Expense", "View Summary", "View Transactions", "Category Report"])

# CSV file path
Data_file = "data.csv"

# Function to load or create CSV file
def load_data():
    if not os.path.exists(Data_file) or os.path.getsize(Data_file)==0:
        df = pd.DataFrame(columns=['amount', 'category', 'date', 'type'])
        df.to_csv(Data_file, index=False)
    return pd.read_csv(Data_file)

# Function to save data
def save_data(amount, category, date, type_):
    new_data = pd.DataFrame([[amount, category, date, type_]], columns=['amount', 'category', 'date', 'type'])
    df = load_data()
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(Data_file, index=False)

# Logic based on menu selection

# Add Income
if menu == "Add Income":
    st.subheader("➕ Add Income")
    with st.form("income_form"):
        amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Salary", "Bonus", "Investment", "Other"])
        date = st.date_input("Date")
        submitted = st.form_submit_button("Save Income")
        if submitted and amount > 0:
            save_data(amount, category, date, "Income")
            st.success("Income saved successfully!")

# Add Expense
elif menu == "Add Expense":
    st.subheader("➖ Add Expense")
    with st.form("expense_form"):
        amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Shopping", "Other"])
        date = st.date_input("Date")
        submitted = st.form_submit_button("Save Expense")
        if submitted and amount > 0:
            save_data(amount, category, date, "Expense")
            st.success("Expense saved successfully!")

# View Summary
elif menu == "View Summary":
    st.subheader("📈 Summary")
    df = load_data()
    income = df[df["type"] == "Income"]["amount"].sum()
    expense = df[df["type"] == "Expense"]["amount"].sum()
    balance = income - expense
    st.metric("Total Income", f"💸 {income:.2f}")
    st.metric("Total Expense", f"💸 {expense:.2f}")
    st.metric("Balance", f"💸 {balance:.2f}")

# View Transactions
elif menu == "View Transactions":
    st.subheader("📜 View Transactions")
    df = load_data()
    st.dataframe(df)

# Category Report
# Category Report
elif menu == "Category Report":
    st.subheader("📉 Expense Category Report")
    df = load_data()
    expense_df = df[df["type"] == "Expense"]
    if not expense_df.empty:
        category_data = expense_df.groupby("category")["amount"].sum()
        category_data.plot.pie(
            autopct="%1.1f%%",
            figsize=(6, 6),
            ylabel="",  # Hide y-axis label
            title="Expenses by Category"
        )
        st.pyplot()  # Call without passing `fig`, as pandas handles it
    else:
        st.info("No expense data available to show pie chart.")

