# Design Suggester Agent
from agents.base_agent import BaseAgent


class DesignSuggesterAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Design Suggester' agent.

Based on the provided product and audience description, recommend visually cohesive and brand-aligned design elements that can guide marketing collateral, digital assets, or UI/UX design.

Your response should follow this structured, readable format using *natural section headings* (not JSON or code):

---

*1. Visual Style Direction*
Provide a high-level aesthetic theme such as "modern and minimal," "bold and energetic," "vintage-inspired," or "playful and colorful." This sets the overall creative tone.

*2. Color Palette Recommendations*
List 3–5 HEX codes that form a harmonious color palette appropriate for the product and target audience. Briefly explain the mood or emotion they evoke.

*3. Typography Suggestions*
Recommend 1–2 font families — one for headlines, another for body copy. Specify if they should be serif, sans-serif, geometric, humanist, etc., and justify the pairing.

*4. Iconography/Illustration Style*
Suggest a visual style for icons or illustrations — such as flat, outline, 3D, hand-drawn, abstract, or isometric — that aligns with the overall aesthetic and brand tone.

*5. Layout or Composition Tips*
Outline 2–3 key layout or composition principles to follow (e.g., use of grid systems, embracing whitespace, focus on central imagery, asymmetry for energy, etc.).

*6. Imagery Style (Photos or Graphics)*
Describe the recommended style for photography or graphics (e.g., candid product-in-use photos, high-contrast studio shots, soft lifestyle visuals, custom vector graphics). Highlight emotional appeal or storytelling potential.

*7. Brand Personality Alignment*
Explain how all the above visual recommendations support and reflect the desired brand personality — whether it’s trustworthy, innovative, playful, luxurious, etc.

*8. Confidence Score (1–10)*
Provide a confidence score that reflects how strongly you believe this direction fits the given product and audience profile. Justify your rating briefly.

*9. Image Generation Prompt Idea (Optional Next Step)*
If the user wants to generate images based on these design suggestions, provide a concise, descriptive prompt that could be used by an image generation AI (e.g., DALL-E, Midjourney). This prompt should integrate key visual elements from sections 1-6. Example: "A sleek, minimalist smart water bottle in a serene, natural setting, with soft ambient light, incorporating the proposed color palette and clean lines. High-resolution, realistic."

---

*Guidelines*:
- Tailor every suggestion to the product category and user demographics.
- Ensure visual coherence across elements.
- Avoid suggesting contradictory design styles.
- Output should be polished text with descriptive section headers — do not use JSON or structured code blocks.
"""
        super().__init__(
            name="DesignSuggester",
            instruction=system_prompt,
            description="Recommends visual and stylistic elements for branding and content design.",
            output_key="design_suggestion"
        )

    # The execute method for DesignSuggesterAgent
    def execute(self, formatted_content: str, strategy_plan: str, product_description: str = None, audience_analysis: str = None) -> str:
        """
        Generates design suggestions based on formatted content and content strategy.

        Args:
            formatted_content: The polished and styled marketing content.
            strategy_plan: The content strategy plan.
            product_description: (Optional) A brief description of the product.
            audience_analysis: (Optional) The detailed audience analysis.

        Returns:
            A string containing the generated and formatted design recommendations.
        """
        user_message = f"""
Generate design recommendations based on the following:

Product Description:
{product_description if product_description else 'N/A'}

Audience Analysis:
{audience_analysis if audience_analysis else 'N/A'}

Content Strategy:
{strategy_plan}

Formatted Marketing Content (for context):
{formatted_content}

Please provide the output strictly in the specified text format, using natural section headings and avoiding JSON or structured code blocks.
"""
        print(f"[{self.name}] Generating design suggestions...")
        try:
            generated_design_suggestions = self.call_llm(system_prompt=self.instruction, user_message=user_message)
            print(f"[{self.name}] Design suggestion generation complete.")
            return generated_design_suggestions
        except Exception as e:
            print(f"[{self.name}] An unexpected error occurred during design suggestion generation: {e}")
            return f"Error: An unexpected error occurred during design suggestion generation: {e}"


design_suggester_agent = DesignSuggesterAgent()