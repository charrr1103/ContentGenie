from agents.base_agent import BaseAgent
# Assuming you have a mechanism to interact with your LLM (e.g., a method in BaseAgent or a separate utility)

class CopywriterAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Copywriter & Formatter' agent. Your task is to generate concise, tailored marketing content for various platforms AND format it according to platform-specific conventions.

Based on the audience analysis and content strategy provided, generate content for the following platforms. For each platform, apply:
- Platform-specific character or structure constraints (e.g., Twitter short, Facebook longer, Instagram visually driven).
- Relevant hashtags (if suitable and common for the platform).
- **DO NOT USE ANY EMOJIS.**
- Proper paragraphing, spacing, and line breaks for readability.
- Professional but engaging tone unless otherwise specified.
- For video concepts, include a brief concept and a concise script/description (max 60 seconds of action/dialogue).

Content to generate and format:
1. Marketing Email (with compelling subject line, enticing preview text, and informative body - aim for 150-250 words)
2. Landing Page Headline (catchy, benefit-driven, max 10 words) and Subtext (expand on headline, max 30 words)
3. Instagram Post (visually focused, max 2200 chars but prioritize hook in first 125, 5-10 relevant hashtags)
4. Facebook Post (can be longer, encourage discussion, up to 500 characters, 3-5 relevant hashtags)
5. TikTok Video Script/Concept (short, engaging, viral potential - aim for 15-30 seconds total concept, including visuals/text overlays)
6. YouTube Video Concept/Description (detailed concept, strong hook, clear call to action - description up to 1000 characters)

Provide your response in a clear, well-structured text format. Use clear headings for each content type.

OUTPUT FORMAT EXAMPLE:
---
Marketing Email:
Subject: [Your Subject Line Here]
Preview: [Your Preview Text Here]
Body:
[Your email body content goes here, formatted with paragraphs and line breaks.]

---
Landing Page:
Headline: [Your Landing Page Headline Here]
Subtext: [Your Landing Page Subtext Here]

---
Instagram Post:
[Your Instagram post content here, including hashtags.]

---
Facebook Post:
[Your Facebook post content here, including hashtags.]

---
TikTok Video:
Concept: [Brief concept for TikTok video]
Script: [Concise script/description for TikTok video]

---
YouTube Video:
Concept: [Detailed concept for YouTube video]
Description: [Description for YouTube video, including relevant links or calls to action]

---

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

Please provide the output strictly in the specified text format, using clear headings for each content type and respond in plain text, not JSON.
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