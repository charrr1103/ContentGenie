# Audience Analyst Agent
from agents.agent import root_agent

class AudienceAnalystAgent(root_agent):
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
        super().__init__("Audience Analyst", system_prompt)
