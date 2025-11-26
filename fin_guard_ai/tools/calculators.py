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