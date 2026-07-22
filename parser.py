import pdfplumber
import re
import os

def clean_extracted_text(raw_text: str) -> str:
    """
    Text ko clean karne ke liye helper function.
    Extra spaces, tabs aur multiple newlines ko single space se replace karta hai.
    """
    if not raw_text:
        return ""
        
    # Multiple spaces/newlines ko single space mein convert karein
    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    
    # Agar document mein ajeeb unicode characters hon to unhe ignore karein (optional)
    # cleaned_text = cleaned_text.encode('ascii', 'ignore').decode('utf-8')
    
    return cleaned_text.strip()

def parse_pdf_cv(file_path: str) -> str:
    """
    PDF file se raw text extract karne ka engine.
    """
    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' nahi mili."

    extracted_text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # extract_text() layout maintain rakhta hai
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        
        # Check agar PDF sirf scanned images par mabni hai (No selectable text)
        if not extracted_text.strip():
            return "Warning: Document empty hai ya scanned image hai (OCR required)."
            
        return clean_extracted_text(extracted_text)
        
    except Exception as e:
        return f"Processing Error: {str(e)}"
