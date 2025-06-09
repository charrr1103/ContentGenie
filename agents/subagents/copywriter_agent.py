from agents.base_agent import BaseAgent

class CopywriterAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Copywriter & Formatter' agent. Your task is to generate concise, tailored marketing content for various platforms AND format it according to platform-specific conventions.

Based on the audience analysis and content strategy provided, generate content for the following platforms. For each platform, apply:
- Platform-specific character or structure constraints.
- Relevant emojis, hashtags (if suitable and common for the platform).
- Proper paragraphing, spacing, and line breaks.
- Professional but engaging tone unless otherwise specified.
- For video concepts, include a brief concept and a script/description.

Content to generate and format:
1. Marketing Email (with subject line, preview text, and body)
2. Landing Page Headline and Subtext
3. Instagram Post
4. Facebook Post
5. TikTok Video Script/Concept
6. YouTube Video Concept/Description

Respond in plain text, not JSON.

OUTPUT FORMAT:

  "MARKETING EMAIL": 
      "Subject": "...",
      "Preview": "...",
      "Body": "..."
  ,
  "LANDING PAGE": 
      "Headline": "...",
      "Subtext": "..."
  ,
  "INSTAGRAM POST": 
      "...",
  "FACEBOOK POST": 
      "...",
  "TIKTOK VIDEO": 
      "Concept": "...",
      "Script": "..."
  ,
  "YOUTUBE VIDEO": 
      "Concept": "...",
      "Description": "..."
  ,
  "TONE": 
      "..."

Only generate text optimized for engagement based on the audience insights and strategy. Keep it punchy, outcome-oriented, and value-focused.
"""
        super().__init__(
            name="CopywriterFormatter",
            instruction=system_prompt,
            description="Generates and formats marketing copy for various digital platforms."
        )
        # You might initialize your LLM here or expect it to be passed via a method
        # self.llm = YourLLMModel() # Example

    def execute(self, audience_analysis: str, content_strategy: str, campaign_goal: str = None, product_description: str = None) -> str:
        """
        Generates marketing copy based on audience analysis and content strategy.

        Args:
            audience_analysis: A string containing the detailed audience analysis.
            content_strategy: A string containing the detailed content strategy plan.
            campaign_goal: (Optional) The primary goal of the marketing campaign.
            product_description: (Optional) A brief description of the product.

        Returns:
            A string containing the generated and formatted marketing content in human-readable text.
        """
        user_message = f"""
Generate marketing content and format it for the following platforms based on the provided information:

Product Description:
{product_description if product_description else 'N/A'}

Campaign Goal:
{campaign_goal if campaign_goal else 'N/A'}

Audience Analysis:
{audience_analysis}

Content Strategy:
{content_strategy}

Please provide the output strictly in the specified text format, using clear headings for each content type.
"""
        print(f"[{self.name}] Generating content...")
        try:
            # Replace 'self.call_llm' with your actual LLM interaction method
            # This method should now return the raw text output.
            generated_content_text = self.call_llm(system_prompt=self.instruction, user_message=user_message)
            print(f"[{self.name}] Content generation complete.")
            return generated_content_text
        except Exception as e:
            print(f"[{self.name}] An unexpected error occurred during content generation: {e}")
            return f"Error: An unexpected error occurred during content generation: {e}"


# Instantiate the agent
copywriter_agent = CopywriterAgent()