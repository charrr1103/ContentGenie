from agents.base_agent import BaseAgent

class AudienceAnalystAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Audience Analyst' agent. Provide a thorough, structured audience analysis based on context.
Format:
{
  "1. Target Audience Persona Summary": { ... },
  "2. Key Insights & Behaviors": { ... },
  "3. Language & Tone Recommendations": { ... },
  "4. Content/Marketing Message Themes": { ... },
  "5. Gaps in Information/Further Research Needs": "",
  "Confidence Score (1-10)": ""
}
"""
        # Corrected super().__init__ call
        # Pass name, and the system_prompt will be set as the instruction
        super().__init__(
            name="AudienceAnalyst",
            instruction=system_prompt, # Pass system_prompt as instruction
            description="Analyzes target audience for marketing campaigns." # Optional, but good practice
            # Do NOT pass model here, it's defined in BaseAgent
        )

audience_analyst_agent = AudienceAnalystAgent()