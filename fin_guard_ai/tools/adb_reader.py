import subprocess
import csv
import io

def fetch_sms_via_adb(limit: int = 20):
    """
    Uses Android Debug Bridge (ADB) to fetch recent SMS messages directly from the connected phone.
    """
    try:
        # The ADB command to query the SMS database
        # We select date, address (sender), and body
        cmd = [
            'adb', 'shell', 'content', 'query', 
            '--uri', 'content://sms/inbox', 
            '--projection', 'date:address:body',
            '--sort', 'date DESC',
            '--limit', str(limit)
        ]
        
        # Run command (shell=True might be needed on Windows depending on path)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            return f"ADB Error: {result.stderr}"
            
        # ADB output format is weird usually: "Row: 0 date=123..., address=..., body=..."
        # We need to parse this raw text into a clean list.
        raw_output = result.stdout
        parsed_sms = []
        
        for line in raw_output.strip().split('\n'):
            if "Row:" in line:
                # Quick and dirty parse (Robust parsing would use regex)
                # This depends heavily on your Android version's output format
                parsed_sms.append(line)
                
        return "\n".join(parsed_sms)

    except FileNotFoundError:
        return "Error: 'adb' command not found. Is Android SDK Platform Tools installed?"
    except Exception as e:
        return f"Error: {str(e)}"

# Test function block
if __name__ == "__main__":
    print(fetch_sms_via_adb())
