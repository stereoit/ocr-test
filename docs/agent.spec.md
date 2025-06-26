# **OCRInvoiceBot: AI Agent Documentation**

This document provides a detailed overview of the OCRInvoiceBot, an AI agent designed to automate the digitalization of invoices from various formats into structured JSON data.

## **1\. Overview**

The OCRInvoiceBot is a specialized AI agent focused on transforming unstructured invoice data (e.g., PDF or JPG images) into a machine-readable, structured JSON format. This enables downstream systems to easily consume and process invoice information without manual data entry. The agent is built upon a modular architecture, leveraging a Large Language Model (LLM) for reasoning and an internal Model Context Protocol (MCP) server for tool exposure and context management.

## **2\. Core Functionality: Digitalize Invoice**

The primary function of the OCRInvoiceBot is digitalize\_invoice. This function performs the following steps:

1. **Input:** Accepts an invoice in PDF or JPG format.
2. **Reasoning:** Utilizes an internal **Connected LLM** that applies a predefined **Instruction Prompt** to understand and extract relevant information from the invoice content.
3. **Structuring:** Based on a strict **JSON Schema**, the LLM's output is structured to ensure consistency and correctness.
4. **Output:** Returns the extracted invoice data as a validated JSON object.

This core functionality is exposed to consumers in two ways:

* **Via MCP.tools capability:** The digitalize\_invoice function is registered as an internal tool within the MCP Server, allowing other MCP-compliant agents or systems to invoke it directly.
* **Via REST Endpoint:** Optionally, the bot exposes a dedicated REST endpoint, /digitize-invoice, providing a standard HTTP interface for external applications to submit invoices and receive structured data.

## **3\. Architectural Components**

The OCRInvoiceBot's architecture is composed of the following key functional blocks:

### **3.1. MCP\_Server**

The Model Context Protocol (MCP) Server acts as the central control plane and context provider for the AI agent. It manages and provides access to essential operational components:

* **Tools:** This repository holds definitions and references to various internal capabilities that the AI agent (specifically the LLM via MCP Tooling) can invoke. The digitalize\_invoice function is registered here as a callable tool.
* **Prompts:** Stores predefined templates and instructions for the LLM. These prompts guide the LLM's reasoning process for specific tasks, such as extracting data from invoices.
* **Resources:** Manages access to external or internal data sources and configurations that the agent might need during its operation (e.g., lookup tables, configuration parameters, specialized OCR models).

### **3.2. AI\_Functions**

This block encapsulates the core artificial intelligence logic and processing capabilities of the bot:

* **JSON Schema:** Defines the expected structure and data types for the output JSON, ensuring that the extracted invoice data is consistent and machine-readable. This schema acts as a guide and validator for the LLM's output.
* **Instruction Prompt:** Represents the specific, dynamically constructed prompt that is fed to the Connected LLM for the current invoice digitalization task. This prompt is typically derived from templates managed in the MCP\_Server/Prompts.
* **MCP Tooling:** This component facilitates the interaction between the Connected LLM and the MCP\_Server's Tools and Resources. It enables the LLM to "call" predefined functions (like external database lookups or specific data processing steps) and access necessary resources during its reasoning process.
* **Connected LLM:** The Large Language Model is the brain of the OCRInvoiceBot. It performs the core reasoning, understanding the invoice content, extracting relevant information, and generating structured data based on the provided Instruction Prompt and guided by the JSON Schema.

### **3.3. REST\_API (Optional)**

The REST API provides an external, standard web interface for the OCRInvoiceBot. Its presence is optional, allowing for flexible deployment scenarios where the bot might solely integrate via MCP in some environments.

* **REST Endpoint 1 (/digitize-invoice):** This is the primary endpoint for external applications to submit invoices (PDF/JPG) and receive the structured JSON output.
* **REST Endpoint 2 (e.g., /status, /health):** Additional endpoints can be exposed for operational monitoring or other client interactions.

## **4\. Interaction and Data Flow**

The following describes the typical data flow for digitalizing an invoice:

1. **Invoice Ingress:** An invoice (PDF/JPG) enters the system.
   * **Option A (via REST API):** An external application sends the invoice to the /digitize-invoice REST endpoint.
   * **Option B (via MCP Tool Invocation):** Another AI agent or system, interacting with the MCP\_Server, invokes the digitalize\_invoice tool, passing the invoice data.
2. **Processing by AI\_Functions:**
   * The AI\_Functions block receives the invoice data.
   * An Instruction Prompt (fetched from MCP\_Server/Prompts) is prepared for the Connected LLM.
   * The Connected LLM processes the invoice content, potentially using MCP Tooling to access Tools or Resources from the MCP\_Server for enhanced reasoning (e.g., verifying vendor information against a database in Resources).
   * The LLM generates preliminary output.
   * The output is then validated against the JSON Schema to ensure it conforms to the required structure.
3. **Structured JSON Output:** The validated JSON data is produced.
4. **Output Egress:**
   * **If invoked via REST API:** The structured JSON is returned as the response to the /digitize-invoice call.
   * **If invoked via MCP Tool:** The structured JSON is returned as the result of the tool invocation within the MCP ecosystem.

This architecture ensures that the core invoice digitalization logic is robust, extensible, and accessible through industry-standard interfaces while maintaining a clear separation of concerns.
