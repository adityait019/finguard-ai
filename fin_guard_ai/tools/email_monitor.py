# tools/email_monitor.py
import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime

def check_for_bank_statements() -> str:
    """
    Checks Gmail for new bank statement emails.
    
    Returns:
        String listing new statements found or 'No new statements'.
    """
    try:
        # Using Gmail API
        creds = Credentials.from_authorized_user_file('token.json')
        service = build('gmail', 'v1', credentials=creds)
        
        # Search for unread emails with "bank statement" in subject
        query = 'subject:(bank statement) is:unread'
        results = service.users().messages().list(userId='me', q=query).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            return "No new bank statements found."
        
        return f"Found {len(messages)} new bank statement(s) to process."
        
    except Exception as e:
        return f"Error checking email: {str(e)}"
