import json
from google.adk.agents import Agent

GEMINI_MODEL = "gemini-2.0-flash"

# --- Visualization Agent that rewrites/summarizes and outputs JSON ---
visualization_agent = Agent(
    name="visualization_agent",
    model=GEMINI_MODEL,
    instruction="""
You are a Visualization AI.

Input: a JSON object with keys:
  - document_summary (string)
  - clauses (array of objects, each with clause_id, summary, risk, etc.)

Task:
1. Rewrite or creatively summarize each clause summary so it's concise and easy to display.
2. Output ONLY valid JSON (no markdown, no code fences, no Mermaid) of this exact structure:

{
  "nodes": [
    {
      "id": "string",         // unique ID for each node
      "label": "string",      // short label for graph
      "summary": "string",    // your rewritten clause summary
      "risk": "string"        // e.g. high / medium / low or descriptive text
    }
  ],
  "edges": [
    {
      "from": "string",       // source node id
      "to": "string",         // target node id
      "relationship": "string"// e.g. follows / summary_of
    }
  ]
}

Important:
- Do not include any extra text outside the JSON.
- Ensure the JSON parses with json.loads in Python.
"""
)

# --- Example usage ---
if __name__ == "__main__":
    # This is the structured JSON you already have from the structuring agent
    structured_json = {
        "document_summary": "Service agreement between client and vendor.",
        "clauses": [
            {
                "clause_id": "C1",
                "summary": "Vendor must deliver software within 30 days.",
                "risk": "High risk of delay"
            },
            {
                "clause_id": "C2",
                "summary": "Client provides required data access.",
                "risk": "Low"
            }
        ]
    }

    # Ask the visualization agent to rewrite and output flowchart JSON
    raw_output = visualization_agent.run(structured_json)

    # Parse to ensure it’s valid JSON
    try:
        visual_json = json.loads(raw_output)
        print(json.dumps(visual_json, indent=2))
    except json.JSONDecodeError:
        raise ValueError("Visualization agent did not return valid JSON:\n" + raw_output)
