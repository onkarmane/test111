import json
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
import google.generativeai as genai
from google import genai

class TenderDetails(BaseModel):
    tender_id: str = Field(description="Unique identifier for the tender.")
    title: str = Field(description="Title or description of the tender.")
    organization: str = Field(description="Name of the organization issuing the tender.")
    closing_date: Optional[date] = Field(description="Date when the tender closes for submission.")
    location: Optional[str] = Field(description="Location where the work is to be performed or where the tender is issued.")
    value: Optional[str] = Field(description="Estimated value or cost of the tender. E.g if value is 50,000 then output 0.5 Lakh")
    contact_person: Optional[str] = Field(description="Name of the contact person for the tender.")
    contact_email: Optional[str] = Field(description="Email address of the contact person.")
    contact_phone: Optional[str] = Field(description="Phone number of the contact person.")
    url: Optional[str] = Field(description="URL or website link related to the tender.")
    category: Optional[str] = Field(description="Category of the tender (e.g., construction, IT, services).")
    document_fees: Optional[str] = Field(description="Fees for obtaining the tender documents. E.g if value is 50,000 then output 0.5 Lakh")
    emd_amount: Optional[str] = Field(description="Earnest Money Deposit (EMD) amount. E.g if value is 50,000 then output 0.5 Lakh")

def extract_tender_details(tender_text: str, api_key: str) -> Optional[TenderDetails]:
    """
    Extracts tender details using the Gemini API.
    """
    

    client = genai.Client(api_key=api_key)

    # response = client.models.generate_content(
    #     model="gemini-2.0-flash", contents="Explain how AI works in a few words"
    # )
    # print(response.text)

    schema = json.dumps(TenderDetails.model_json_schema())
    prompt = f"""
    Please extract the following information from the provided tender text and return the results in a structured JSON format using the schema defined below.

    Schema:
    {schema}

    Tender Text:
    {tender_text}

    Output (JSON):
    """

    try:
        # response = client.models.generate_content(model="gemini-pro", contents=prompt)
        response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
        result = response.text
        if result.startswith("```json"):
            result = result[7:-3]

        print("Gemini Output:", result)  # Debugging: print the raw output
        tender_details = TenderDetails.model_validate_json(result)
        return tender_details
    except json.JSONDecodeError:
        print("Error: invalid JSON response from Gemini.")
        return None
    except Exception as e:
        print(f"Error parsing Gemini output: {e}")
        return None

tender_text = """
TENDER NOTICE

Tender ID: IND/PWD/2024/0045
Subject: Construction of Reinforced Concrete Bridge over River Kaveri
Organization: Public Works Department, Government of Karnataka
Location: Ramanagara District, Karnataka, India
Closing Date: 2024-07-26, 15:00 IST
Estimated Value: INR 12,50,00,000 (Indian Rupees Twelve Crore Fifty Lakhs Only)
Category: Civil Engineering, Bridge Construction

The Public Works Department (PWD), Government of Karnataka, invites sealed tenders from eligible and qualified contractors for the construction of a reinforced concrete bridge over the River Kaveri in Ramanagara District. The scope of work includes, but is not limited to, the construction of bridge substructure, superstructure, approach roads, and related ancillary works as per the detailed specifications provided in the tender document.

Tender documents can be downloaded from the e-procurement portal: www.eproc.karnataka.gov.in. Bidders are required to register on the portal to participate in the tender.

Document Fees: INR 10,000 (Non-refundable)
EMD Amount: INR 25,00,000 (Indian Rupees Twenty-Five Lakhs Only)

Pre-bid Meeting: A pre-bid meeting will be held on 2024-06-15 at 11:00 IST in the office of the Chief Engineer, PWD, Bangalore.

Contact Person: Mr. Ramesh Kumar, Executive Engineer
Contact Email: ramesh.kumar.pwd@karnataka.gov.in
Contact Phone: +91 80 2225 3456

Note: The PWD reserves the right to accept or reject any or all tenders without assigning any reason thereof.
"""

api_key = "AIzaSyD8Y5MdpQCH_fdJjcS4Nkt9RvDRmUizrHk" # Replace with your API key

tender_details = extract_tender_details(tender_text, api_key)

if tender_details:
    print(tender_details)
