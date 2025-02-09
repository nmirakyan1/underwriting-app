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
        "NOI (Final Year)": cash_flows[-1],
        "Cap Rate": cap_rate,
        "Exit Value": exit_value,
        "Annual Cash Flows": cash_flows,
        "Net Cash Flow (After Debt)": net_cash_flow,
        "Total Debt Payments": total_debt_payments,
        "Total Profit": total_profit,
        "Deal ROI": roi,
        "Cash on Cash Return": cash_on_cash_return,
        "CoC Annualized": coc_annualized,
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
    
    st.write(f"**🏢 Purchase Price:** ${purchase_price:,.2f}")
    st.write(f"**✅ NOI (Final Year):** ${result['NOI (Final Year)']:.2f}")
    st.write(f"**📈 Cap Rate:** {result['Cap Rate']:.2%}")
    st.write(f"**🏢 Exit Value:** ${result['Exit Value']:.2f}")
    st.write(f"**💳 Total Debt Payments:** ${result['Total Debt Payments']:.2f}")
    st.write(f"**💰 Total Profit:** ${result['Total Profit']:.2f}")
    st.write(f"**📊 ROI:** {result['Deal ROI']:.2f}%")
    st.write(f"**📉 Cash on Cash Return:** {result['Cash on Cash Return']:.2f}%")
    st.write(f"**📅 Annualized CoC:** {result['CoC Annualized']:.2f}%")
    st.write(f"**⏳ Estimated Timeframe:** {result['Estimated Timeframe (Months)']} months")

    # Display Annual Cash Flow in Table Format
    st.subheader("💰 Annual Cash Flow Projections")
    cash_flow_df = pd.DataFrame({
        "Year": [i + 1 for i in range(len(result["Annual Cash Flows"]))],
        "Annual Cash Flow ($)": result["Annual Cash Flows"],
        "Net Cash Flow After Debt ($)": result["Net Cash Flow (After Debt)"]
    })
    st.table(cash_flow_df)
