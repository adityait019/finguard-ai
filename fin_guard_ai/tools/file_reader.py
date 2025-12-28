import os
import pandas as pd

def read_bank_statement(filename: str) -> str:
    """
    Reads a bank statement CSV file from the 'resources' directory.
    
    Args:
        filename: The name of the file (e.g., 'statement_nov.csv').
        
    Returns:
        A string representation of the transaction data.
    """
    try:
        # Securely construct path (prevent traversing up directories)
        base_path = os.getcwd()
        file_path = os.path.join(base_path, 'fin_guard_ai','resources', filename)
        
        if not os.path.exists(file_path):
            return f"Error: File '{filename}' not found in resources folder."
            
        # Read CSV using pandas
        # df = pd.read_csv(file_path)
        df=pd.read_excel(file_path)
        
        # Return as a formatted string LLM can understand
        return df.to_string(index=False)
        
    except Exception as e:
        return f"Error reading file: {str(e)}"
