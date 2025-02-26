
---

### **2️⃣ Output for Each Document**
Using the extracted data from the uploaded PDFs:

#### **Document 1: Sample_American_RE_company.pdf**
- **Total Fleet:** 114
- **Annual Mileage:** 2,128,374
- **Reimbursed Mileage:** Not provided
- **State:** OR & WA (Reimbursement Rate = 0.8)

**Calculation:**
- `PPT = 2,128,374 / (0.8 * 15,000) ≈ 177.36`

**Decision:**
- Since **114 < 177.36**, **Decision = "Decline"**.

---

#### **Document 2: Sample15.pdf**
- **Total Fleet:** 100
- **Annual Mileage:** Not provided
- **Reimbursed Mileage:** 100,000
- **State:** CO & UT (Reimbursement Rate = 0.655)

**Calculation:**
- `PPT = 100,000 / (0.655 * 15,000) ≈ 10.18`

**Decision:**
- Since **100 > 10.18**, **Decision = "Approve"**.

---

### **3️⃣ Python Script for Evaluation**
This script:
✅ Extracts key data points from the PDFs  
✅ Performs manual calculations  
✅ Calls the AI model  
✅ Compares AI results with manual calculations  

```python
import json
import openai
import pdfplumber
import re

# Ensure OpenAI API Key is set
openai.api_key = "your-api-key-here"  # Replace with actual key

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    """Extracts text from a given PDF file using pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to parse extracted text
def parse_insurance_data(text):
    """Parses key insurance data points from extracted PDF text."""
    fleet_match = re.search(r"FLEET:\s*(\d+)", text)
    total_fleet = int(fleet_match.group(1)) if fleet_match else None

    mileage_match = re.search(r"HNO annual mileage:\s*([\d,]+)", text)
    annual_mileage = int(mileage_match.group(1).replace(',', '')) if mileage_match else None

    reimbursed_match = re.search(r"REIMBURSED MILEAGE:\s*([\d,]+)", text)
    reimbursed_mileage = int(reimbursed_match.group(1).replace(',', '')) if reimbursed_match else None

    state_match = re.search(r"State breakout\s*–\s*([\w\s&]+)", text)
    states = state_match.group(1).strip().split("&") if state_match else []

    return {
        "total_fleet": total_fleet,
        "annual_mileage": annual_mileage,
        "reimbursed_mileage": reimbursed_mileage,
        "states": [state.strip() for state in states]
    }

# Function to calculate PPT
def calculate_ppt(data):
    """Computes PPT based on available mileage data."""
    DEFAULT_RATE = 0.655
    SPECIAL_RATE_STATES = ["OR", "WA"]
    SPECIAL_RATE = 0.8

    rate = SPECIAL_RATE if any(state in SPECIAL_RATE_STATES for state in data["states"]) else DEFAULT_RATE

    if data["annual_mileage"]:
        ppt = data["annual_mileage"] / 15000
    elif data["reimbursed_mileage"]:
        ppt = data["reimbursed_mileage"] / (rate * 15000)
    else:
        ppt = None
    
    return ppt

# Function to validate AI decision
def call_ai_for_decision(data):
    """Calls LLM API to validate the AI-generated decision."""
    ai_prompt = """You are an AI assistant evaluating insurance applications. Follow these steps:
    1. Extract:
       - Total Fleet
       - Annual Mileage (if provided)
       - Reimbursed Mileage (if provided)
       - State Information
    2. Perform calculations:
       - PPT Calculation as per rules.
    3. Decision:
       - If Total Fleet > PPT, return "Approve"
       - Else return "Decline"
    Return JSON output:
    {
        "total_fleet": <value>,
        "ppt": <calculated_ppt>,
        "decision": "<Approve/Decline>"
    }
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": ai_prompt},
            {"role": "user", "content": json.dumps(data)}
        ]
    )

    ai_output = json.loads(response["choices"][0]["message"]["content"])
    return {
        "ai_decision": ai_output["decision"],
        "manual_decision": data["decision"],
        "is_correct": ai_output["decision"] == data["decision"]
    }

# Processing PDF files
pdf_files = {
    "Sample_American_RE_company.pdf": "/mnt/data/Sample_American_RE_company.pdf",
    "Sample15.pdf": "/mnt/data/Sample15.pdf"
}

# Extract text from PDFs
extracted_data = {name: extract_text_from_pdf(path) for name, path in pdf_files.items()}
print("\nExtracted Data:", extracted_data)

# Parse extracted text
parsed_data = {name: parse_insurance_data(text) for name, text in extracted_data.items()}
print("\nParsed Data:", parsed_data)

# Compute PPT & Decision
for name, data in parsed_data.items():
    ppt = calculate_ppt(data)
    data["ppt"] = ppt
    data["decision"] = "Approve" if data["total_fleet"] > ppt else "Decline"
    print(f"\nFinal Decision for {name}: {data['decision']} (PPT: {ppt})")

# Validate AI Decision
for name, data in parsed_data.items():
    validation_result = call_ai_for_decision(data)
    print(f"\nAI Decision for {name}: {validation_result['ai_decision']}, Correct: {validation_result['is_correct']}")
    print("\nValidation Result:", validation_result)
