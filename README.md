# Invoice Parser MCP Agent

This agent extracts structured data from invoices using a Large Language Model (LLM). It is designed to be run as a Model Context Protocol (MCP) resource.

## Overview

The agent receives invoice content (currently expected as text, with OCR for images as a planned extension), sends it to a configured LLM along with a detailed system prompt and a JSON schema, and then validates the LLM's JSON response against this schema.

The core functionalities are:
-   Parsing invoice data for fields like vendor/customer details, IDs (VAT, Tax, ICO, DIC), dates, line items, and totals.
-   Utilizing an external LLM for the extraction logic.
-   Validating the output against a predefined JSON schema (`invoice_schema.json`).

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
*   **Update `invoice_parser_agent.py`:**
    *   Modify the `call_llm_expert` function to include the API calls to your chosen LLM.
    *   You might pass LLM configuration (API keys, model names, endpoints) via environment variables, a configuration file, or through the `llm_config` dictionary passed to `extract_invoice_data`.
*   **Install LLM SDK:** Add the necessary Python library for your chosen LLM to `requirements.txt` and install it.

**Example (Conceptual for Gemini):**

In `invoice_parser_agent.py`, `call_llm_expert` might look like:

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
*   **Update `invoice_parser_agent.py`:** Uncomment and adapt the OCR section in `extract_invoice_data`.

## Running the Agent

The agent's core logic is in `invoice_parser_agent.py`. To run it as an MCP agent, you'll need to use the `modelcontextprotocol/python-sdk`.

A conceptual integration is provided in the comments of `invoice_parser_agent.py`. You would typically:
1.  Complete the `InvoiceParsingAgent` class by inheriting from the SDK's base `Agent` class.
2.  Implement the `process_request` method as outlined.
3.  Use the SDK's utilities to start the agent server.

**Example (Conceptual, assuming SDK provides `run_agent`):**

```python
# In invoice_parser_agent.py (or a new main.py)
if __name__ == "__main__":
    from modelcontextprotocol.agent import Agent # Or specific imports
    # from modelcontextprotocol.server import run_agent # Hypothetical SDK function

    # Assuming InvoiceParsingAgent class is defined as in the conceptual comments

    # You'll need to get the actual SDK classes and functions
    # For example:
    # from modelcontextprotocol.runner import run
    # from your_agent_module import InvoiceParsingAgent

    # agent_instance = InvoiceParsingAgent(agent_id="invoice-parser", version="0.1.0")
    # print("Starting Invoice Parser Agent...")
    # run(agent_instance, host="0.0.0.0", port=8080) # Replace with actual SDK run command

    # For now, you can test the core logic directly:
    print("Running invoice_parser_agent.py in direct test mode (not as MCP agent):")
    # This will execute the __main__ block within invoice_parser_agent.py
    import subprocess
    subprocess.run(["python", "invoice_parser_agent.py"])

```

Once the agent server is running (e.g., on `http://localhost:8080`), it's ready to be added as an MCP resource.

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

The agent returns a JSON object conforming to `invoice_schema.json`.

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
*   **OCR:** For image-based invoices, robust OCR (e.g., Tesseract, Google Cloud Vision API, Azure Computer Vision) is crucial for good quality text extraction before sending to the LLM.
*   **Error Handling:** Enhance error handling for LLM API calls, OCR failures, and validation issues.
*   **Schema Evolution:** The `invoice_schema.json` can be extended as needed to capture more fields or support different invoice structures.
*   **Security:** Be mindful of API key management. Use environment variables or secure secret management solutions; do not hardcode keys in the source code.
*   **Testing `invoice_parser_agent.py`:** The `if __name__ == "__main__":` block in `invoice_parser_agent.py` allows you to test the core extraction logic directly by running `python invoice_parser_agent.py`. The dummy LLM response will be used.
```
