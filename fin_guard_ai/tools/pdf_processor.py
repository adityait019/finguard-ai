# tools/pdf_processor.py
import os
from pypdf import PdfReader
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(override=True)
statement_path=Path(r"C:\Users\adity\project\agent capstone\fin_guard_ai\resources\statements")
def unlock_statement_pdf(file_path: str) -> str:
    """
    Unlocks password-protected bank statement PDF.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Status message
    """
    try:
        password = os.getenv('SBI_STATEMENT_PASSWORD', 'default_password')
        
        reader = PdfReader(file_path)
        
        if reader.is_encrypted:
            reader.decrypt(password)
        
        # Extract text from all pages
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        
        return text
        
    except Exception as e:
        return f"Error unlocking PDF: {str(e)}"


print(unlock_statement_pdf(str(statement_path / "8966227954531072025.pdf")))