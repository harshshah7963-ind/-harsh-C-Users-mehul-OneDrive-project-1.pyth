import streamlit as st
import pandas as pd
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# -----------------------------
# Session State Initialization
# -----------------------------
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# -----------------------------
# Sidebar Navigation
# -----------------------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# -----------------------------
# Home Page
# -----------------------------
if menu == "Home":

    st.title("💰 Expense Tracker Application")

    st.markdown("""
    ### Welcome to Expense Tracker

    This web application helps users manage their daily income and expenses efficiently.

    ### Features
    - Add Income
    - Add Expenses
    - View Transactions
    - Track Balance
    - Category-wise Expense Summary

    ### Purpose
    The main purpose of this application is to help users understand
    where their money is being spent and manage finances better.
    """)

# -----------------------------
# Add Transaction Page
# -----------------------------
elif menu == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.radio(
        "Select Transaction Type",
        ["Income", "Expense"]
    )

    # Income Form
    if transaction_type == "Income":

        source = st.text_input("Income Source")
        amount = st.number_input("Amount", min_value=0.0)
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description")

        if st.button("Add Income"):

            transaction = {
                "Type": "Income",
                "Category/Source": source,
                "Amount": amount,
                "Date": transaction_date.strftime("%d-%m-%Y"),
                "Description": description
            }

            st.session_state.transactions.append(transaction)

            st.success("Income Added Successfully!")

    # Expense Form
    else:

        category = st.selectbox(
            "Expense Category",
            ["Food", "Travel", "Shopping", "Bills",
             "Education", "Medical", "Others"]
        )

        amount = st.number_input("Amount", min_value=0.0)
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_area("Description")

        if st.button("Add Expense"):

            transaction = {
                "Type": "Expense",
                "Category/Source": category,
                "Amount": amount,
                "Date": transaction_date.strftime("%d-%m-%Y"),
                "Description": description
            }

            st.session_state.transactions.append(transaction)

            st.success("Expense Added Successfully!")

# -----------------------------
# View Transactions Page
# -----------------------------
elif menu == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(df, use_container_width=True)

    else:
        st.warning("No transactions available.")

# -----------------------------
# Summary Page
# -----------------------------
elif menu == "Summary":

    st.title("📊 Financial Summary")

    transactions = st.session_state.transactions

    if transactions:

        df = pd.DataFrame(transactions)

        # Total Income
        total_income = df[df["Type"] == "Income"]["Amount"].sum()

        # Total Expense
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

        # Balance
        balance = total_income - total_expense

        # Display Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Income", f"₹ {total_income:.2f}")
        col2.metric("Total Expenses", f"₹ {total_expense:.2f}")
        col3.metric("Balance", f"₹ {balance:.2f}")

        st.divider()

        # Category-wise Expense Summary
        st.subheader("📌 Category-wise Expense Summary")

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_summary = (
                expense_df.groupby("Category/Source")["Amount"]
                .sum()
                .reset_index()
            )

            category_summary.columns = ["Category", "Total Spent (₹)"]

            st.table(category_summary)

        else:
            st.info("No expense data available.")

    else:
        st.warning("No transactions available.")