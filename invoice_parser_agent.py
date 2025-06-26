import json
import os
from jsonschema import validate, ValidationError

# --- Configuration ---
SCHEMA_FILE_PATH = 'invoice_schema.json' # Path to the JSON schema file

# --- Load JSON Schema ---
def load_schema(schema_path):
    """Loads the JSON schema from the specified file."""
    try:
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        return schema
    except FileNotFoundError:
        print(f"Error: Schema file not found at {schema_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from schema file {schema_path}")
        raise

INVOICE_SCHEMA = load_schema(SCHEMA_FILE_PATH)

# --- System Prompt ---
SYSTEM_PROMPT_TEMPLATE = """
You are an invoice data extractor. From the provided invoice representation (text or image data), perform these tasks:

- Parse the data.
- Look for invoice-related fields such as VAT, TAX ID, ICO, DIC, addresses, references, list of items, prices, and any related data to an invoice document.

Respond back ONLY with a valid JSON object that strictly follows this schema:

```json
{{response_schema_definition}}
```

Ensure all string values in the JSON are properly escaped.
If a field is not present in the invoice, set its value to null (unless the schema specifies it's required and has no default or null type).
For dates, use YYYY-MM-DD format.
For numbers, use standard decimal representation (e.g., 123.45). Do not include currency symbols within the number values themselves; use the dedicated 'currency' field.
"""

def get_system_prompt():
    """Returns the system prompt with the schema definition embedded."""
    schema_string = json.dumps(INVOICE_SCHEMA, indent=2)
    return SYSTEM_PROMPT_TEMPLATE.replace("{{response_schema_definition}}", schema_string)

# --- LLM Interaction (Placeholder) ---
def call_llm_expert(prompt: str, invoice_content: str, llm_config: dict = None):
    """
    Placeholder function to simulate calling an external LLM.
    In a real implementation, this function would:
    1. Take invoice_content (text or image data) and the prompt.
    2. Make an API call to the chosen LLM (e.g., Gemini, Mistral, OpenAI model).
    3. Handle potential API errors.
    4. Return the LLM's response (expected to be a JSON string).

    For now, it will return a dummy JSON string for testing purposes.
    """
    print("--- LLM Interaction (Placeholder) ---")
    print(f"System Prompt Length: {len(prompt)}")
    print(f"Invoice Content Snippet: {invoice_content[:200]}...") # Print a snippet

    # TODO: Replace this with actual LLM API call
    # Example:
    # if llm_config.get("type") == "gemini":
    #   from google.cloud import aiplatform
    #   from google.cloud.aiplatform.gapic.types import HarmCategory, HarmBlockThreshold
    #   # ... initialize Gemini model and make prediction
    #   pass
    # elif llm_config.get("type") == "huggingface_api":
    #   import requests
    #   # ... make request to Hugging Face Inference API
    #   pass

    print("Warning: Using placeholder LLM response.")
    dummy_response = {
        "invoice_id": "INV-2023-001",
        "issue_date": "2023-10-26",
        "due_date": "2023-11-25",
        "vendor_name": "Example Corp",
        "vendor_address": "123 Main St, Anytown, USA",
        "vendor_vat_id": "US123456789",
        "vendor_tax_id": None,
        "vendor_ico": None,
        "vendor_dic": None,
        "vendor_bank_account": "1234567890",
        "vendor_swift_bic": "EXMPUS33",
        "customer_name": "Test Customer Ltd.",
        "customer_address": "456 Oak Ave, Otherville, USA",
        "customer_vat_id": None,
        "customer_tax_id": None,
        "customer_ico": None,
        "customer_dic": None,
        "line_items": [
            {
                "description": "Product A",
                "quantity": 2,
                "unit_price": 50.00,
                "total_price": 100.00,
                "vat_rate": 0.10,
                "vat_amount": 10.00
            },
            {
                "description": "Service B",
                "quantity": 1,
                "unit_price": 75.00,
                "total_price": 75.00,
                "vat_rate": 0.10,
                "vat_amount": 7.50
            }
        ],
        "subtotal": 175.00,
        "total_tax_amount": 17.50,
        "total_amount": 192.50,
        "currency": "USD",
        "payment_terms": "Net 30 days",
        "notes": "Thank you for your business!",
        "raw_text": invoice_content if isinstance(invoice_content, str) else "Image data provided"
    }
    return json.dumps(dummy_response)

# --- Response Validation ---
def validate_invoice_data(invoice_data_json):
    """
    Validates the extracted invoice data against the JSON schema.
    Returns the parsed JSON object if valid, otherwise raises ValidationError.
    """
    try:
        if isinstance(invoice_data_json, str):
            invoice_data = json.loads(invoice_data_json)
        else:
            invoice_data = invoice_data_json # Assuming it's already a dict

        validate(instance=invoice_data, schema=INVOICE_SCHEMA)
        print("Invoice data is valid against the schema.")
        return invoice_data
    except json.JSONDecodeError as e:
        print(f"Error: LLM output is not valid JSON. Details: {e}")
        print(f"LLM Output causing error: {invoice_data_json[:500]}...") # Print snippet of problematic JSON
        raise
    except ValidationError as e:
        print(f"Error: Invoice data failed schema validation. Details: {e.message}")
        print(f"Data: {invoice_data}") # Print data that failed validation
        # For more detailed error path:
        # print(f"Path: {list(e.path)}")
        # print(f"Schema Path: {list(e.schema_path)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during validation: {e}")
        raise


# --- Main Processing Function ---
def extract_invoice_data(invoice_content: str, llm_config: dict = None):
    """
    Extracts structured data from invoice content (text or path to image).

    Args:
        invoice_content (str): Can be raw text extracted from an invoice or
                               a path to an invoice image file.
                               If it's a path, this function will need to be
                               extended with OCR capabilities.
        llm_config (dict, optional): Configuration for the LLM.
                                     Example: {"type": "gemini", "api_key": "..."}
                                     Defaults to None, using the placeholder.

    Returns:
        dict: A dictionary containing the extracted invoice data, conforming to the schema.
              Returns None if extraction or validation fails.
    """
    # TODO: Add OCR logic if invoice_content is an image path
    # For now, we assume invoice_content is text.
    # Example using Tesseract (requires installation and pytesseract library):
    # if os.path.isfile(invoice_content) and invoice_content.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
    #     try:
    #         import pytesseract
    #         from PIL import Image
    #         invoice_text_content = pytesseract.image_to_string(Image.open(invoice_content))
    #         print(f"Successfully OCR'd image: {invoice_content}")
    #     except ImportError:
    #         print("Pytesseract or Pillow not installed. Please install for OCR functionality.")
    #         print("Falling back to treating content as text.")
    #         invoice_text_content = f"Content of image file: {invoice_content} (OCR not performed)"
    #     except Exception as e:
    #         print(f"Error during OCR: {e}")
    #         return None
    # else:
    #     invoice_text_content = invoice_content # Assume it's already text

    invoice_text_content = invoice_content # Current assumption

    system_prompt = get_system_prompt()

    try:
        llm_response_json = call_llm_expert(system_prompt, invoice_text_content, llm_config)
        parsed_invoice_data = validate_invoice_data(llm_response_json)
        return parsed_invoice_data
    except (ValidationError, json.JSONDecodeError) as e:
        print(f"Could not process invoice due to validation/decode error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred in extract_invoice_data: {e}")
        return None

# --- Example Usage (for testing) ---
if __name__ == "__main__":
    print("--- Running Invoice Parser Agent (Test Mode) ---")

    # 1. Test with sample text
    sample_invoice_text = """
    Invoice #123
    Date: 2024-07-15
    From: Supplier Inc., 1 Business Rd, Commerce City
    To: Customer Co., 2 Client Ave, Market Town
    Item: Widget, Qty: 5, Unit Price: 10.00, Total: 50.00
    Item: Gadget, Qty: 2, Unit Price: 25.00, Total: 50.00
    Subtotal: 100.00
    Tax (10%): 10.00
    Total: 110.00 USD
    Vendor VAT: EU123456789
    """
    print("\n--- Test 1: Processing sample invoice text ---")
    # In a real scenario, the system prompt is part of the LLM call, not directly here
    # For the dummy LLM, it doesn't use the prompt in its logic currently.
    extracted_data = extract_invoice_data(sample_invoice_text)

    if extracted_data:
        print("\nSuccessfully extracted and validated invoice data:")
        print(json.dumps(extracted_data, indent=2))
    else:
        print("\nFailed to extract or validate invoice data from text.")

    # 2. Test with schema (to ensure it loads)
    print(f"\n--- System Prompt for LLM (first 500 chars) ---")
    print(get_system_prompt()[:500] + "...")

    # 3. Test validation with deliberately bad data
    print("\n--- Test 2: Testing validation with incorrect data type ---")
    bad_data_type = json.dumps({
        "vendor_name": "Test Vendor",
        "total_amount": "NOT_A_NUMBER" # Incorrect type
    })
    try:
        validate_invoice_data(bad_data_type)
    except ValidationError:
        print("Correctly caught ValidationError for bad data type.")
    except Exception as e:
        print(f"Unexpected error during bad data type test: {e}")

    print("\n--- Test 3: Testing validation with missing required field ---")
    bad_missing_field = json.dumps({
        # "vendor_name": "Test Vendor", # Missing required field
        "total_amount": 100.00
    })
    try:
        validate_invoice_data(bad_missing_field)
    except ValidationError:
        print("Correctly caught ValidationError for missing required field.")
    except Exception as e:
        print(f"Unexpected error during missing field test: {e}")

    print("\n--- End of Test Mode ---")

"""
MCP Integration (Conceptual - to be implemented in a wrapper or main agent file)

from modelcontextprotocol.agent import Agent, AgentContext, AgentRequest, AgentResponse

class InvoiceParsingAgent(Agent):
    async def process_request(self, context: AgentContext, request: AgentRequest) -> AgentResponse:
        if request.resource_name != "invoice_parser":
            return AgentResponse.error(f"Unknown resource: {request.resource_name}")

        invoice_content = request.body.get("invoice_content") # Expecting text or image path
        llm_config = request.body.get("llm_config") # Optional LLM config

        if not invoice_content:
            return AgentResponse.error("Missing 'invoice_content' in request body.")

        try:
            # In a real agent, you might handle file uploads for images,
            # perform OCR if needed, then pass text to extract_invoice_data.
            # For now, assuming invoice_content is text.

            extracted_data = extract_invoice_data(invoice_content, llm_config)

            if extracted_data:
                return AgentResponse.success(body=extracted_data)
            else:
                return AgentResponse.error("Failed to extract invoice data after processing.")
        except Exception as e:
            print(f"Error processing request in InvoiceParsingAgent: {e}")
            return AgentResponse.error(f"Internal server error: {str(e)}")

# To run this agent (example, depends on SDK specifics):
# if __name__ == "__main__":
#   agent = InvoiceParsingAgent(agent_id="invoice-parser-agent", version="0.1.0")
#   # ... SDK-specific server setup and run command ...
#   # e.g., agent.serve(host="0.0.0.0", port=8080)
"""
