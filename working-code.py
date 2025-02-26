import pdfplumber
import re
import json
import openai

# Ensure OpenAI API Key is set
openai.api_key = "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"
# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

# Function to parse extracted text
def parse_insurance_data(text):
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
    return ai_output["decision"] == data["decision"]

# Processing PDF files
pdf_files = {
    "Sample_American_RE_company.pdf": "C:\\MLCourse\\Input_data\\Sample_American_RE_company.pdf",
    "Sample15.pdf": "C:\\MLCourse\\Input_data\\Sample15.pdf"
}

# Extract text from PDFs
extracted_data = {name: extract_text_from_pdf(path) for name, path in pdf_files.items()}
print("\nExtracted Data:\n", extracted_data)

# Parse extracted text
parsed_data = {name: parse_insurance_data(text) for name, text in extracted_data.items()}
print("\nParsed Data:\n", parsed_data)

# Compute PPT & Decision
for name, data in parsed_data.items():
    ppt = calculate_ppt(data)
    data["ppt"] = ppt
    data["decision"] = "Approve" if data["total_fleet"] > ppt else "Decline"
    print(f"\nFinal Decision for {name}: {data['decision']} (PPT: {ppt})")

# Validate AI Decision
for name, data in parsed_data.items():
    is_correct = call_ai_for_decision(data)
    print(f"\nAI Decision for {name}: {is_correct}")
