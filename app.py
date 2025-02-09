import numpy as np
import pandas as pd

def calculate_underwriting(
    purchase_price, 
    rent_per_sf, 
    property_size, 
    annual_expenses, 
    expense_growth_rate,
    lease_term,
    exit_cap_rate,
    annual_rent_growth,
    loan_amount=0,
    interest_rate=0,
    loan_term=0
):
    """
    AI Underwriting Calculation for Retail/Industrial Properties.
    Returns NOI, Cap Rate, and Cash Flow Projections.
    """
    
    # Calculate Gross Rental Income
    annual_rent = rent_per_sf * property_size
    cash_flows = []
    
    for year in range(lease_term):
        # Apply rent escalation
        annual_rent *= (1 + annual_rent_growth)
        
        # Apply expense inflation
        annual_expenses *= (1 + expense_growth_rate)
        
        # Calculate Net Operating Income (NOI)
        noi = annual_rent - annual_expenses
        
        cash_flows.append(noi)
    
    # Calculate Cap Rate
    cap_rate = cash_flows[-1] / purchase_price
    
    # Calculate Exit Value
    exit_value = cash_flows[-1] / exit_cap_rate
    
    # Loan Payments (if applicable)
    if loan_amount > 0:
        loan_payment = (loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -loan_term)
        net_cash_flow = [noi - loan_payment for noi in cash_flows]
    else:
        net_cash_flow = cash_flows
    
    return {
        "NOI (Final Year)": cash_flows[-1],
        "Cap Rate": cap_rate,
        "Exit Value": exit_value,
        "Annual Cash Flows": cash_flows,
        "Net Cash Flow (After Debt)": net_cash_flow
    }

# Example Run
result = calculate_underwriting(
    purchase_price=2000000,
    rent_per_sf=20,
    property_size=15000,
    annual_expenses=50000,
    expense_growth_rate=0.03,
    lease_term=10,
    exit_cap_rate=0.06,
    annual_rent_growth=0.02,
    loan_amount=1000000,
    interest_rate=0.05,
    loan_term=20
)

# Display results
result
