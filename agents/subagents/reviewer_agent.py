import os
from agents.base_agent import BaseAgent
from PIL import Image

class ReviewerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Reviewer' agent. Your task is to evaluate the entire content pipeline including:

1. Audience Profile
2. Strategy Plan
3. Marketing Copy
4. Visual Design Suggestions
5. (Optional) Actual Image

Audience Analysis:
{audience_analysis}

Content Strategy:
{content_strategy}

Marketing Copy:
{marketing_copy}

Design Suggestion:
{design_suggestion}

Based on the output from each component:

- Take entire component output.
- DO NOT summarize the component output.
- Preserve and review entire component output not summarize them. 
- Modify and improve the component contents in terms of grammar, clarity and tone.
- Give suggestions and explain why suggest so after modifying the parts.
- If unchanged, repeat the original exactly under `modified`.
- Score it from 1 to 10 based on clarity, alignment with goal, and usefulness for the campaign.
- Strictly follow the output format for each components.
- Do not skip any output for any components in term of length or brevity

---

REQUIRED OUTPUT FORMAT (for all components except image):
- Bold the header (e.g. Original "<component>", Suggestion)
- Leave 2 lines after each components

Original "<component>":
<entire original content>

Original "<component>" score:
<score from 1 to 10>

Modified "<component>":
<full content with specific edits, OR repeat original if no changes>

Suggestion:
<describe what was changed or why no change was needed>

For "image_generation_result", omit `modified`, but include:

original "image_generation_result":
[IMAGE DISPLAYED: path]
<image analysis text from Gemini>

original "image_generation_result" score:
<1–10>

suggestion:
<describe visual improvement or confirm visual alignment>

- Respond in plain text, follow structure exactly.
- DO NOT truncate the response

"""    

        super().__init__(
            name="ContentReviewer",
            instruction=system_prompt,
            description="Reviews full marketing pipeline and embeds image in the visual review section."
        )

        




    def execute(
        self,
        audience_analysis: str,
        content_strategy: str,
        marketing_copy: str,
        design_suggestion: str,
        image_generation_output: dict = None
    ) -> str:
        """
        Full multimodal review, includes displaying the image file.

        Args:
            audience_analysis: Entire text result from audience_analyst.
            content_strategy: Entire text result from content_strategist.
            marketing_copy: Entire text result from copywriter.
            design_suggestion: text result from design_suggester.
            image_generation_output: Output dict from image_generator_agent.

        Returns:
            Structured review output.
        """
        image_review_text = "No image provided."
        image_path_display = "[No image file path]"

        if image_generation_output and image_generation_output.get("status") == "success":
            filename = image_generation_output.get("filename")
            image_path = os.path.join("generated_images", filename)
            image_path_display = f"[IMAGE DISPLAYED: {image_path}]"

            if os.path.exists(image_path):
                try:
                    with Image.open(image_path) as img:
                        vision_response = gemini_model.generate_content([
                            img,
                            "Evaluate this marketing image. Does it align with modern branding? Consider layout, color, and tone consistency with the copy and design plan."
                        ])
                        image_review_text = vision_response.text
                except Exception as e:
                    image_review_text = f"[Image processing error: {e}]"

        # Build the review prompt
        user_message = f"""
original "audience_profile":
{audience_analysis}

original "strategy_summary":
{content_strategy}

original "marketing_copy":
{marketing_copy}

original "design_recommendations":
{design_suggestion}

original "image_generation_result":
{image_path_display}
{image_review_text}

For each component, respond with:

- original "<component>"
- original "<component>" score (1-10)
- modified "<component>"  ← OMIT for image
- suggestion
"""
        print(f"[{self.name}] Reviewing full content with image embed...")
        try:
            review_output = self.call_llm(system_prompt=self.instruction, user_message=user_message)
            print(f"[{self.name}] Review complete.")
            return review_output
        except Exception as e:
            print(f"[{self.name}] An error occurred during review: {e}")
            return f"Error: An error occurred during review: {e}"

   
# Instantiate
reviewer_agent = ReviewerAgent()
