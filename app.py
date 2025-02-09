import streamlit as st
import pandas as pd

def calculate_underwriting(
    purchase_price, rent_per_sf, property_size, annual_expenses, 
    expense_growth_rate, lease_term, exit_cap_rate, annual_rent_growth, 
    loan_amount=0, interest_rate=0, loan_term=0
):
    # Calculate Gross Rental Income
    annual_rent = rent_per_sf * property_size
    cash_flows = []

    for year in range(lease_term):
        annual_rent *= (1 + annual_rent_growth)
        annual_expenses *= (1 + expense_growth_rate)
        noi = annual_rent - annual_expenses
        cash_flows.append(noi)

    # Cap Rate & Exit Value
    cap_rate = cash_flows[-1] / purchase_price
    exit_value = cash_flows[-1] / exit_cap_rate

    # Loan Payments (if applicable)
    if loan_amount > 0:
        loan_payment = (loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -loan_term)
        net_cash_flow = [noi - loan_payment for noi in cash_flows]
    else:
        net_cash_flow = cash_flows

    # Additional Financial Metrics
    total_debt_payments = loan_payment * loan_term if loan_amount > 0 else 0
    total_profit = exit_value - purchase_price - total_debt_payments
    roi = (total_profit / purchase_price) * 100
    cash_on_cash_return = (total_profit / loan_amount) * 100 if loan_amount > 0 else 0
    coc_annualized = cash_on_cash_return / lease_term

    return {
        "Purchase Price": purchase_price,
        "Total Debt Payments": total_debt_payments,
        "Net Operating Income": cash_flows[-1],
        "Sale Closing Costs": exit_value * 0.04,
        "All In Cost": purchase_price + total_debt_payments,
        "Equity Needed": purchase_price * 0.3,
        "Target Sale": exit_value,
        "Total Profit": total_profit,
        "Deal ROI": roi,
        "LP Pref": total_profit * 0.2,
        "LP Split": total_profit * 0.5,
        "Total LP Returns": total_profit * 0.7,
        "Cash on Cash Return": cash_on_cash_return,
        "CoC Annualized": coc_annualized,
        "XIRR": coc_annualized * 0.8,
        "Estimated Timeframe (Months)": lease_term * 12
    }

# Streamlit UI
st.title("AI Underwriting Tool for Retail & Industrial Properties")

# User Inputs
purchase_price = st.number_input("Purchase Price ($)", value=1700000)
rent_per_sf = st.number_input("Rent per SF ($)", value=20.0)
property_size = st.number_input("Property Size (SF)", value=15398)
annual_expenses = st.number_input("Annual Expenses ($)", value=50000)
expense_growth_rate = st.number_input("Expense Growth Rate (%)", value=3.0) / 100
lease_term = st.number_input("Lease Term (Years)", value=5)
exit_cap_rate = st.number_input("Exit Cap Rate (%)", value=6.0) / 100
annual_rent_growth = st.number_input("Annual Rent Growth (%)", value=2.0) / 100

loan_amount = st.number_input("Loan Amount ($)", value=1000000)
interest_rate = st.number_input("Loan Interest Rate (%)", value=5.0) / 100
loan_term = st.number_input("Loan Term (Years)", value=20)

# Streamlit UI for Displaying Results
if st.button("Calculate"):
    result = calculate_underwriting(
        purchase_price, rent_per_sf, property_size, annual_expenses, 
        expense_growth_rate, lease_term, exit_cap_rate, annual_rent_growth, 
        loan_amount, interest_rate, loan_term
    )
    
    # Properly display results in Streamlit
    st.subheader("📊 Underwriting Results")
    
    for key, value in result.items():
        if isinstance(value, float):
            formatted_value = f"${value:,.2f}" if key not in ["Deal ROI", "Cash on Cash Return", "CoC Annualized", "XIRR"] else f"{value:.2f}%"
        else:
            formatted_value = value
        st.write(f"**{key}:** {formatted_value}")
