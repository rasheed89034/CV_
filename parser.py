import pdfplumber
import re
import os

def clean_extracted_text(raw_text: str) -> str:

    if not raw_text:
        return ""
        

    cleaned_text = re.sub(r'\s+', ' ', raw_text)
    
   
    
    return cleaned_text.strip()

def parse_pdf_cv(file_path: str) -> str:

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
