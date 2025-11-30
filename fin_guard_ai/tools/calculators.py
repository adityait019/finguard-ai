def calculate_compound_interest(principal: float, rate: float, years: int) -> str:
    """
    Calculates compound interest.
    
    Args:
        principal: The initial amount of money (e.g., 1000).
        rate: The annual interest rate as a percentage (e.g., 5 for 5%).
        years: The number of years the money is invested.
        
    Returns:
        A string summary of the investment growth.
    """
    try:
        # Convert percentage to decimal
        r = rate / 100
        amount = principal * (1 + r) ** years
        interest_earned = amount - principal
        
        return (f"After {years} years, an investment of ${principal:,.2f} "
                f"at {rate}% will grow to ${amount:,.2f}. "
                f"Total interest earned: ${interest_earned:,.2f}.")
    except Exception as e:
        return f"Error calculating interest: {str(e)}"


def calculate_emi(principal: float, annual_rate: float, tenure_months: int) -> dict:
    """
    Calculate Equated Monthly Installment (EMI) for loans.
    
    Args:
        principal: Loan amount in rupees
        annual_rate: Annual interest rate (percentage, e.g., 8.5 for 8.5%)
        tenure_months: Loan tenure in months
    
    Returns:
        Dictionary with EMI, total payment, and total interest
    """
    monthly_rate = (annual_rate / 100) / 12
    
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
    
    total_payment = emi * tenure_months
    total_interest = total_payment - principal
    
    return {
        "emi": round(emi, 2),
        "total_payment": round(total_payment, 2),
        "total_interest": round(total_interest, 2),
        "principal": principal,
        "monthly_rate_percent": round(monthly_rate * 100, 4)
    }
