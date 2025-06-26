# Invoice Parser MCP Agent

This agent extracts structured data from invoices using a Large Language Model (LLM). It is designed to be run as a Model Context Protocol (MCP) resource.

## Overview

The agent receives invoice content (currently expected as text, with OCR for images as a planned extension), sends it to a configured LLM along with a detailed system prompt and a JSON schema, and then validates the LLM's JSON response against this schema.

The core functionalities are:
-   Parsing invoice data for fields like vendor/customer details, IDs (VAT, Tax, ICO, DIC), dates, line items, and totals.
-   Utilizing an external LLM for the extraction logic.
-   Validating the output against a predefined JSON schema (`src/invoice_parser_agent/schema.json`).

## Setup Instructions

### 1. Python Environment

It's recommended to use a virtual environment:

```bash
python -m venv venv
# On Windows
# venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```
(Note: `requirements.txt` currently includes `jsonschema`. You will need to add dependencies for your chosen LLM SDK, e.g., `google-cloud-aiplatform` for Gemini, `openai` for OpenAI models, or `requests` for Hugging Face API, and potentially OCR libraries like `Pillow` and `pytesseract`.)

### 2. LLM Configuration (Placeholder - To Be Implemented)

This agent uses a placeholder for LLM interaction. To connect to a real LLM, you will need to:

*   **Choose an LLM and Platform:**
    *   **Google Gemini:** Via Vertex AI. Requires `google-cloud-aiplatform` and authentication (e.g., service account key).
    *   **OpenAI Models (GPT-3.5/4):** Requires the `openai` library and an API key.
    *   **Hugging Face Models:** Can be accessed via the Inference API (`requests`) or by running models locally/on a dedicated instance (`transformers`).
*   **Update `src/invoice_parser_agent/agent_logic.py`:**
    *   Modify the `call_llm_expert` function in `src/invoice_parser_agent/agent_logic.py` to include the API calls to your chosen LLM.
    *   You might pass LLM configuration (API keys, model names, endpoints) via environment variables, a configuration file, or through the `llm_config` dictionary passed to `extract_invoice_data`.
*   **Install LLM SDK:** Add the necessary Python library for your chosen LLM to `requirements.txt` and install it.

**Example (Conceptual for Gemini):**

In `src/invoice_parser_agent/agent_logic.py`, `call_llm_expert` might look like:

```python
# from google.cloud import aiplatform
# from google.cloud.aiplatform.gapic.types import HarmCategory, HarmBlockThreshold

# def call_llm_expert(prompt: str, invoice_content: str, llm_config: dict = None):
#     project = llm_config.get("project_id")
#     location = llm_config.get("location", "us-central1")
#     model_name = llm_config.get("model_name", "gemini-1.5-flash-001") # Or your preferred model

#     aiplatform.init(project=project, location=location)
#     model = aiplatform.GenerativeModel(model_name)

#     full_prompt = f"{prompt}\n\nInvoice Content:\n{invoice_content}"

#     response = model.generate_content(
#         [full_prompt],
#         generation_config={"response_mime_type": "application/json"}, # Crucial for Gemini
#         # safety_settings={ # Optional: configure safety settings
#         #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#         # }
#     )
#     return response.text # Gemini returns JSON string directly if response_mime_type is set
```

### 3. OCR Configuration (Optional Extension)

If you plan to process invoice images, you'll need an OCR engine. The current code has placeholders for `pytesseract`.
*   **Install Tesseract OCR Engine:** Follow instructions for your OS from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract).
*   **Install Python Libraries:**
    ```bash
    pip install Pillow pytesseract
    ```
*   **Update `src/invoice_parser_agent/agent_logic.py`:** Uncomment and adapt the OCR section in `extract_invoice_data` within `src/invoice_parser_agent/agent_logic.py`.

## Project Structure

The project is structured as follows:

```
.
├── src/
│   └── invoice_parser_agent/
│       ├── __init__.py                 # Makes it a Python package
│       ├── agent_logic.py              # Core data extraction logic, LLM calls
│       ├── mcp_agent.py                # MCP SDK integration (Agent class)
│       └── schema.json                 # JSON schema for invoice data
├── examples/
│   ├── example_invoice.txt           # Sample invoice text
│   └── expected_output.json          # Expected JSON output for the sample (from dummy LLM)
├── tests/                            # Optional: For future unit tests
│   └── ...
├── main.py                           # Entry point to run the MCP agent server
├── README.md                         # This file
└── requirements.txt                  # Python dependencies
```

## Running the Agent

The agent is designed to be run using the `modelcontextprotocol/python-sdk`. The MCP integration is handled in `src/invoice_parser_agent/mcp_agent.py`, and the core parsing logic is in `src/invoice_parser_agent/agent_logic.py`.

A top-level `main.py` is provided as the primary entry point to start the agent server.

1.  **Ensure SDK is Set Up:**
    *   The `src/invoice_parser_agent/mcp_agent.py` file contains placeholder classes for the MCP SDK (`Agent`, `AgentContext`, etc.). You will need to replace these with the actual imports from the `modelcontextprotocol` SDK once it's installed and available in your environment.
    *   The `main.py` script will also need to use the correct functions from the SDK to run the agent.

2.  **Run the Agent Server:**
    Once the SDK is correctly integrated, you would typically run:
    ```bash
    python main.py
    ```
    This script should initialize and start the `InvoiceParsingAgent` server (e.g., on `http://localhost:8080`).

### Testing Core Logic Directly

You can test the core data extraction logic (using the placeholder LLM) by running the `agent_logic.py` script directly:
```bash
python src/invoice_parser_agent/agent_logic.py
```
This will execute its `if __name__ == "__main__":` block, which processes sample text and validates against the schema.

Once the agent server is running via `main.py` (e.g., on `http://localhost:8080`), it's ready to be added as an MCP resource.

## VS Code MCP Integration

To add this agent as an MCP resource in Visual Studio Code (assuming you have the Model Context Protocol extension installed):

1.  **Open VS Code Settings:**
    *   Go to `File > Preferences > Settings` (or `Code > Settings > Settings` on macOS).
    *   Alternatively, use the shortcut `Ctrl+,` (or `Cmd+,`).
2.  **Search for MCP Settings:**
    *   In the search bar, type `mcp resources`.
3.  **Edit `settings.json`:**
    *   Find the setting `ModelContextProtocol.Server: Resources` (the exact name might vary slightly based on the extension version).
    *   Click on "Edit in settings.json".
4.  **Add Agent Configuration:**
    *   Add a new entry to the `modelContextProtocol.server.resources` array (or create the array if it doesn't exist).
    *   The configuration for this agent would look something like this:

    ```json
    "modelContextProtocol.server.resources": [
        // ... other resources if any ...
        {
            "name": "InvoiceExtractor", // A user-friendly name for VS Code
            "displayName": "Invoice Data Extractor (Python)",
            "description": "Extracts structured data from invoices.",
            "agent": {
                // Assuming your agent runs on localhost port 8080
                "url": "http://localhost:8080"
            },
            "doc": {
                // Optional: URL to this README or other documentation
                // "url": "https://github.com/your-repo/path/to/README.md"
            },
            "resourcePatterns": [
                // Define patterns for when this agent should be suggested or used.
                // This is highly dependent on how you want to invoke it.
                // Example: if you want to right-click a file and send its content:
                "**/invoices/*.txt",
                "**/scans/*.png",
                "**/scans/*.jpg"
            ],
            "capabilities": {
                // Describe what the agent can do.
                // The MCP extension might use this to filter agents.
                "can_process_text": true,
                "can_process_image": true, // Set to true if OCR is implemented
                "output_format": "application/json"
            },
            "request": {
                // Defines how VS Code should structure the request to your agent.
                // This needs to match what your agent's `process_request` expects.
                "resourceName": "invoice_parser", // Should match agent's expected resource_name
                "body": {
                    // "invoice_content": "${fileContent}" // Send content of the active/selected file
                    // "invoice_content": "${filePath}" // Or send file path (agent needs to read file)
                    "invoice_content": "${selection}", // Send selected text
                    // You might also want to allow users to specify llm_config if needed
                    // "llm_config": { "model_name": "gemini-pro-vision" } // Example
                }
            }
        }
    ]
    ```

    **Explanation of `request.body` options:**
    *   `"${fileContent}"`: VS Code will send the entire content of the file matched by `resourcePatterns`.
    *   `"${filePath}"`: VS Code will send the path to the matched file. Your agent would then need to read this file. (Good for images if OCR is local).
    *   `"${selection}"`: VS Code will send the currently selected text in the editor.
    *   Choose the option that best fits your agent's input handling. For text-based invoices, `"${selection}"` or `"${fileContent}"` are good. For images, `"${filePath}"` (if agent does OCR) or a mechanism to send image data (e.g. base64 `"${fileContentAsBase64}"` if supported by MCP extension) would be needed. The example above defaults to `"${selection}"`.

5.  **Save `settings.json`**.

The agent should now be available in the VS Code MCP extension, invocable based on the `resourcePatterns` and the request structure you defined.

## Input/Output Format

### Input

The agent's `process_request` method (when integrated with MCP SDK) expects a JSON body with:

*   `invoice_content`: (string) This can be:
    *   The raw text extracted from an invoice.
    *   A path to an invoice image file (if OCR is implemented and the agent is coded to handle file paths).
    *   Base64 encoded image data (if the agent is coded to handle this).
*   `llm_config`: (object, optional) A dictionary containing configuration for the LLM (e.g., API keys, model names). This is passed to `extract_invoice_data`.

**Example MCP Request Body:**

```json
{
  "invoice_content": "Invoice #789 Date: 2023-11-01 From: Test Co ...",
  "llm_config": {
    "type": "gemini",
    "model_name": "gemini-1.5-flash-001"
    // Potentially API keys or other auth info if not handled by environment
  }
}
```

### Output

The agent returns a JSON object conforming to `src/invoice_parser_agent/schema.json`.

**Example Successful Response Body:**

```json
{
  "invoice_id": "INV-2023-001",
  "issue_date": "2023-10-26",
  // ... other fields as per schema ...
  "total_amount": 192.50,
  "currency": "USD"
}
```

**Example Error Response Body:**

```json
{
  "error": "Failed to extract invoice data after processing."
  // Or a more specific error message
}
```

## Development Notes

*   **LLM Choice:** The placeholder `call_llm_expert` needs to be replaced with actual calls to your chosen LLM. Consider models with strong JSON output capabilities and good instruction following. Gemini models with `response_mime_type: "application/json"` are excellent for this.
*   **OCR:** For image-based invoices, robust OCR (e.g., Tesseract, Google Cloud Vision API, Azure Computer Vision) is crucial for good quality text extraction before sending to the LLM. This would be implemented in `src/invoice_parser_agent/agent_logic.py`.
*   **Error Handling:** Enhance error handling for LLM API calls, OCR failures, and validation issues in `src/invoice_parser_agent/agent_logic.py` and `src/invoice_parser_agent/mcp_agent.py`.
*   **Schema Evolution:** The `src/invoice_parser_agent/schema.json` can be extended as needed to capture more fields or support different invoice structures. Remember to update the system prompt in `agent_logic.py` if the schema changes significantly.
*   **Security:** Be mindful of API key management. Use environment variables or secure secret management solutions; do not hardcode keys in the source code.
*   **Testing Core Logic:** The `if __name__ == "__main__":` block in `src/invoice_parser_agent/agent_logic.py` allows you to test the core extraction logic directly by running `python src/invoice_parser_agent/agent_logic.py`. The dummy LLM response will be used.
*   **MCP SDK Integration:** The `src/invoice_parser_agent/mcp_agent.py` and `main.py` files will need to be updated with actual imports and functions from the `modelcontextprotocol/python-sdk` when it's available.
```
