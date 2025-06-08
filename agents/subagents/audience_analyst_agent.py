from agents.base_agent import BaseAgent

class AudienceAnalystAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Audience Analyst' agent. Provide a structured audience analysis with the following sections:
- Target Audience Persona Summary
- Key Insights & Behaviors
- Language & Tone Recommendations
- Content/Marketing Message Themes
- Gaps in Information or Further Research Needs
Also include a Confidence Score from 1–10 at the end.
Respond in plain text, not JSON.
"""
        # Corrected super().__init__ call
        # Pass name, and the system_prompt will be set as the instruction
        super().__init__(
            name="AudienceAnalyst",
            instruction=system_prompt, # Pass system_prompt as instruction
            description="Analyzes target audience for marketing campaigns."
        )

audience_analyst_agent = AudienceAnalystAgent()