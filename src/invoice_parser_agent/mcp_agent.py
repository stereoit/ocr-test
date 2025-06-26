"""
MCP Agent Implementation for Invoice Parsing.
This file contains the agent class that integrates with the
Model Context Protocol Python SDK.
"""
# from modelcontextprotocol.agent import Agent, AgentContext, AgentRequest, AgentResponse
# For now, using placeholder classes to allow for linting and conceptual structure
class AgentContext: # Placeholder
    pass
class AgentRequest: # Placeholder
    def __init__(self, resource_name, body):
        self.resource_name = resource_name
        self.body = body
class AgentResponse: # Placeholder
    @staticmethod
    def success(body):
        print(f"AgentResponse.success: {body}")
        return {"status": "success", "body": body}
    @staticmethod
    def error(message):
        print(f"AgentResponse.error: {message}")
        return {"status": "error", "message": message}

class Agent: # Placeholder
    def __init__(self, agent_id, version):
        self.agent_id = agent_id
        self.version = version
        print(f"Agent initialized: {agent_id} v{version}")


# Adjust the import path based on the new file structure
from .agent_logic import extract_invoice_data #, get_system_prompt is not directly used by agent shell

class InvoiceParsingAgent(Agent):
    """
    MCP Agent for parsing invoice data.
    """
    def __init__(self, agent_id="invoice-parser-agent", version="0.1.1"):
        super().__init__(agent_id, version)

    async def process_request(self, context: AgentContext, request: AgentRequest) -> AgentResponse:
        """
        Processes an incoming request to parse an invoice.
        """
        # context.logger.info(f"Received request for resource: {request.resource_name}") # Example logging

        if request.resource_name != "invoice_parser": # Or a more specific/configurable resource name
            # context.logger.warn(f"Unknown resource requested: {request.resource_name}")
            return AgentResponse.error(f"Unknown resource: {request.resource_name}")

        invoice_content = request.body.get("invoice_content") # Expecting text, image path, or base64 image bytes
        llm_config = request.body.get("llm_config") # Optional LLM config

        if not invoice_content:
            # context.logger.error("Missing 'invoice_content' in request body.")
            return AgentResponse.error("Missing 'invoice_content' in request body.")

        try:
            # context.logger.info(f"Starting invoice data extraction for content type: {type(invoice_content)}")
            # In a real agent, you might handle:
            # - File uploads for images (if request.body is multipart/form-data)
            # - Base64 encoded image data passed in JSON
            # - Perform OCR if needed (e.g. if invoice_content is image bytes or path)
            # Then pass the extracted text to extract_invoice_data.

            extracted_data = extract_invoice_data(invoice_content, llm_config)

            if extracted_data:
                # context.logger.info("Successfully extracted and validated invoice data.")
                return AgentResponse.success(body=extracted_data)
            else:
                # context.logger.error("Failed to extract invoice data after processing (e.g. validation failed).")
                return AgentResponse.error("Failed to extract and validate invoice data.")
        except Exception as e:
            # context.logger.error(f"Error processing request in InvoiceParsingAgent: {e}", exc_info=True)
            print(f"Error processing request in InvoiceParsingAgent: {e}") # Basic print for now
            return AgentResponse.error(f"Internal server error: {str(e)}")

# Conceptual: How this agent might be run (e.g., in a main.py or using SDK tools)
# if __name__ == "__main__":
#   from modelcontextprotocol.server import run_agent # Hypothetical SDK function
#
#   agent_instance = InvoiceParsingAgent()
#   print(f"Starting {agent_instance.agent_id} v{agent_instance.version}...")
#   # The SDK would provide a way to run the agent, e.g.:
#   # run_agent(agent_instance, host="0.0.0.0", port=8080)
#
#   # For testing the placeholder classes:
#   print("\n--- Conceptual MCP Agent Test ---")
#   test_agent = InvoiceParsingAgent()
#   dummy_request_body = {
#       "invoice_content": "Sample invoice text...",
#       "llm_config": {"type": "dummy"}
#   }
#   dummy_request = AgentRequest(resource_name="invoice_parser", body=dummy_request_body)
#   dummy_context = AgentContext()
#
#   import asyncio
#   response = asyncio.run(test_agent.process_request(dummy_context, dummy_request))
#   print(f"Conceptual agent response: {response}")
#   print("--- End Conceptual MCP Agent Test ---")

```
