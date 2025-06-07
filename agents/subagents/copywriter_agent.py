from agents.base_agent import BaseAgent

class CopywriterAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Copywriter' agent. Based on the audience analysis provided, generate concise, tailored marketing content for the following platforms:
1. LinkedIn Post
2. Marketing Email (with subject line and body)
3. Landing Page Headline and Subtext

Format your response as:
{
  "LinkedIn Post": "...",
  "Marketing Email": {
    "Subject": "...",
    "Body": "..."
  },
  "Landing Page": {
    "Headline": "...",
    "Subtext": "..."
  },
  "Tone": "..."
}
Only generate text optimized for engagement based on the audience insights. Keep it punchy, outcome-oriented, and value-focused.
"""
        # Corrected super().__init__ call
        super().__init__(
            name="Copywriter",
            instruction=system_prompt, # Pass system_prompt as instruction
            description="Drafts marketing copy for various platforms." # Optional
        )

# Instantiate the agent
copywriter_agent = CopywriterAgent()