"""
IMPROVED PDF EXTRACTOR FOR REMITTANCE ADVICE
This version handles the format shown in your PDF better
"""

import re

def extract_remittance_data(text):
    """
    Extract remittance data from PDF text
    Handles formats like:
    - Invoice No INV-101
    - Invoice Date 28-Dec-2025  
    - Invoice Amount Rs 45,000
    """
    
    print("🔍 IMPROVED EXTRACTION STARTING...")
    print(f"📄 Text length: {len(text)} characters")
    
    # Normalize text
    normalized_text = re.sub(r'\s+', ' ', text)
    print(f"📄 Normalized text: {normalized_text[:300]}...")
    
    data = {
        "Invoice Number": "Not Found",
        "Invoice Date": "Not Found",
        "Total Amount": "Not Found"
    }
    
    # ==================== INVOICE NUMBER ====================
    # Patterns for this specific PDF format
    inv_patterns = [
        r'Invoice\s+No[:\s]+([A-Z0-9-]+)',          # Invoice No INV-101
        r'Invoice\s+Number[:\s]+([A-Z0-9-]+)',       # Invoice Number INV-101
        r'Invoice\s+No\.\s*([A-Z0-9-]+)',            # Invoice No. INV-101
        r'INV-(\d+)',                                 # Direct INV-123 pattern
    ]
    
    for pattern in inv_patterns:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            if 'INV-' in match.group(0).upper():
                data["Invoice Number"] = match.group(0).split()[-1]  # Get last part
            else:
                data["Invoice Number"] = f"INV-{match.group(1)}"
            print(f"✓ Found Invoice Number: {data['Invoice Number']}")
            break
    
    # ==================== INVOICE DATE ====================
    date_patterns = [
        # DD-MMM-YYYY format (28-Dec-2025)
        r'Invoice\s+Date[:\s]+(\d{1,2}-[A-Za-z]{3}-\d{4})',
        # DD Month YYYY (28 December 2025)
        r'Invoice\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]+\s+\d{4})',
        # DD-MM-YYYY (28-12-2025)
        r'Invoice\s+Date[:\s]+(\d{1,2}-\d{1,2}-\d{4})',
        # Any date after "Invoice Date"
        r'Invoice\s+Date[:\s]+([^\n\r]+?)(?:\s|$)',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            date_str = match.group(1).strip()
            # Clean up - remove extra spaces and text
            date_str = re.sub(r'\s+', ' ', date_str)
            # Take only the date part (stop at next field)
            date_str = date_str.split('Invoice')[0].split('Amount')[0].strip()
            if len(date_str) > 5 and len(date_str) < 30:  # Reasonable date length
                data["Invoice Date"] = date_str
                print(f"✓ Found Invoice Date: {data['Invoice Date']}")
                break
    
    # ==================== TOTAL AMOUNT ====================
    amount_patterns = [
        # Rs 45,000 or Rs. 45,000
        r'(?:Invoice\s+)?Amount[:\s]+Rs\.?\s*([\d,]+(?:\.\d{2})?)',
        # INR 45,000 or INR 45000
        r'(?:Invoice\s+)?Amount[:\s]+INR\.?\s*([\d,]+(?:\.\d{2})?)',
        # Just number after "Amount"
        r'(?:Invoice\s+)?Amount[:\s]+([\d,]+(?:\.\d{2})?)',
        # Rs anywhere followed by amount
        r'Rs\.?\s+([\d,]+(?:\.\d{2})?)',
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, normalized_text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).strip()
            # Validate it's a reasonable number
            clean_amount = amount_str.replace(',', '')
            try:
                amount_value = float(clean_amount)
                if amount_value > 0:  # Must be positive
                    data["Total Amount"] = amount_str
                    print(f"✓ Found Total Amount: {data['Total Amount']}")
                    break
            except:
                continue
    
    print(f"\n✅ EXTRACTION COMPLETE:")
    print(f"   Invoice Number: {data['Invoice Number']}")
    print(f"   Invoice Date: {data['Invoice Date']}")
    print(f"   Total Amount: {data['Total Amount']}")
    
    return data


# Test with the known PDF content
if __name__ == "__main__":
    # This is the content from your PDF
    test_text = """
    Remittance Advice
    Remittance No RA-001
    Remittance Date 05-Jan-2026
    Payer Name ABC Pharma Pvt. Ltd.
    Payee Name XYZ Suppliers
    Invoice No INV-101
    Invoice Date 28-Dec-2025
    Invoice Amount Rs 45,000
    Paid Amount Rs 45,000
    Payment Mode NEFT
    Transaction ID TXN1001
    """
    
    print("=" * 80)
    print("TEST EXTRACTION")
    print("=" * 80)
    result = extract_remittance_data(test_text)
    print("\n" + "=" * 80)
    print("FINAL RESULT:")
    print("=" * 80)
    for key, value in result.items():
        print(f"{key}: {value}")