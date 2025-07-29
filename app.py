# library
import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ---------- CSS Styling ----------
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- Session State Setup ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- Helper Functions ----------
def get_user_file(username):
    return f"data_{username}.csv"

def load_data(username):
    file = get_user_file(username)
    if not os.path.exists(file) or os.path.getsize(file) == 0:
        df = pd.DataFrame(columns=['amount', 'category', 'date', 'type'])
        df.to_csv(file, index=False)
    return pd.read_csv(file)

def save_data(username, amount, category, date, type_):
    new_data = pd.DataFrame([[amount, category, str(date), type_]],
                            columns=['amount', 'category', 'date', 'type'])
    df = load_data(username)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(get_user_file(username), index=False)

def filter_data(df, period):
    df['date'] = pd.to_datetime(df['date'])
    today = datetime.today()
    if period == "This Week":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return df[(df['date'] >= start) & (df['date'] <= end)]
    elif period == "This Month":
        return df[df['date'].dt.month == today.month]
    else:
        return df

# ---------- Login Section ----------
def login_section():
    st.title("🔐 Login to Personal Finance Tracker")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if username and password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Please enter both username and password.")

# ---------- Main App ----------
def finance_app():
    st.sidebar.title(f"👤 Hello, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Sidebar Menu and Filter
    menu = st.sidebar.selectbox("Select Option", [
        "Add Income", "Add Expense", "View Summary", "View Transactions", "Category Report"
    ])
    filter_option = st.sidebar.radio("View data for:", ["All", "This Week", "This Month"])

    username = st.session_state.username
    df = load_data(username)
    filtered_df = filter_data(df, filter_option)

    # Add Income
    if menu == "Add Income":
        st.subheader("➕ Add Income")
        with st.form("income_form"):
            amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
            category = st.selectbox("Category", ["Salary", "Bonus", "Extra Income", "Other"])
            date = st.date_input("Date")
            submitted = st.form_submit_button("Save Income")
            if submitted and amount > 0:
                save_data(username, amount, category, date, "Income")
                st.success("Income saved successfully!")

    # Add Expense
    elif menu == "Add Expense":
        st.subheader("➖ Add Expense")
        with st.form("expense_form"):
            amount = st.number_input("Enter amount", min_value=0.0, format="%.2f")
            category = st.selectbox("Category", ["Food", "Rent", "Utilities","Invesment" ,"Shopping", "Other"])
            date = st.date_input("Date")
            submitted = st.form_submit_button("Save Expense")
            if submitted and amount > 0:
                save_data(username, amount, category, date, "Expense")
                st.success("Expense saved successfully!")

    # View Summary
    elif menu == "View Summary":
        st.subheader("📈 Summary")
        income = filtered_df[filtered_df["type"] == "Income"]["amount"].sum()
        expense = filtered_df[filtered_df["type"] == "Expense"]["amount"].sum()
        balance = income - expense
        st.metric("Total Income", f"💸 {income:.2f}")
        st.metric("Total Expense", f"💸 {expense:.2f}")
        st.metric("Balance", f"💸 {balance:.2f}")

    # View Transactions
    elif menu == "View Transactions":
        st.subheader("📜 View Transactions")
        st.dataframe(filtered_df)

    # Category Report with bar_chart (deployment-ready)
    elif menu == "Category Report":
        st.subheader("📉 Expense Category Report")
        expense_df = filtered_df[filtered_df["type"] == "Expense"]
        if not expense_df.empty:
            category_data = expense_df.groupby("category")["amount"].sum()
            st.write("💡 Expense amount by category:")
            st.bar_chart(category_data)
        else:
            st.info("No expense data available to show chart.")

# ---------- App Entry ----------
if not st.session_state.logged_in:
    login_section()
else:
    finance_app()
