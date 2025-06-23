import os
import io
from agents.base_agent import BaseAgent
from PIL import Image
from google.cloud import storage
import google.generativeai as genai
import re

# GCS Client setup
gcs_client = storage.Client()

# Gemini model setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-pro-latest")

class ReviewerAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are the 'Reviewer' agent. Your task is to evaluate the entire content pipeline including:

1. Audience Analysis
2. Content Strategy
3. Marketing Copy
4. Design Suggestion
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

- Take entire component output as input.
- Preserve and review entire component output not summarize them or curtail them. 
- Modify and improve the component contents in terms of grammar, clarity and tone.
- Give suggestions and explain why suggest so after modifying the parts.
- If unchanged, repeat the original exactly under `modified`.
- Score it from 1 to 10 based on clarity, alignment with goal, and usefulness for the campaign.
- Strictly follow the output format for each components.
- You MUST repeat the full original text under **Original "<component>":**


DO NOT:
- DO NOT summarize the component output.
- DO NOT remove for brevity
- DO NOT provide a summarisation as a output (e.g. The marketing copy is generally well-written and aligned with the target audience. Minor tweaks could be made to personalize it further (e.g., incorporating specific fitness goals into the email/landing page copy). The examples provided cover a good range of platforms and content formats. The design suggestions are comprehensive and well-suited to the target audience. The color palette, typography choices, and imagery style all contribute to a modern, healthy, and convenient brand image. The inclusion of an image generation prompt is helpful for visualizing the desired aesthetic. No changes needed.)
- DO NOT shorten the any component output
- Do not use ... to skip any content
- DO NOT summarize or say "See original above"
- DO NOT omit any part of the original content
---

REQUIRED OUTPUT FORMAT (for all components except image):
- Bold the header (e.g. Original "<component>", Suggestion)
- Blank 3 lines after each components suggestion

**Original "strategy_summary":**
This campaign is designed to build brand awareness...

**Original "strategy_summary" score:**
8

**Modified "strategy_summary":**
This campaign aims to boost visibility...

**Suggestion:**
Improved tone and reduced wordiness. Clearer goal linkage.


<br><br><br>

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
- Respond as if the reviewer and the consumer cannot scroll up. Repeat everything required.

"""    

        super().__init__(
            name="ContentReviewer",
            instruction=system_prompt,
            description="Reviews full marketing pipeline and embeds image in the visual review section."
        )

    def _load_image_from_gcs(self, gcs_uri: str) -> Image.Image:
        """Download and return image as PIL.Image from a GCS URI"""
        bucket_name, blob_path = gcs_uri.replace("gs://", "").split("/", 1)
        bucket = gcs_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        img_bytes = blob.download_as_bytes()
        return Image.open(io.BytesIO(img_bytes))    

    def execute(
        self,
        audience_analysis: str,
        content_strategy: str,
        marketing_copy: str,
        design_suggestion: str,
        image_generation_output: dict = None,
        tool_context=None
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

        """
        Full review including visual image analysis from GCS.
        """

        image_path_display = "[No image provided]"
        image_review_text = "No image included for evaluation."

        if image_generation_output and image_generation_output.get("status") == "success":
            gcs_uri = image_generation_output.get("gcs_uri")
            if gcs_uri:
                image_path_display = f"[IMAGE DISPLAYED: {gcs_uri}]"
                try:
                    image = self._load_image_from_gcs(gcs_uri)
                    gemini_response = gemini_model.generate_content([
                        image,
                        "Evaluate this image for branding tone, clarity, layout, and marketing effectiveness."
                    ])
                    image_review_text = gemini_response.text
                except Exception as e:
                    image_review_text = f"[Error loading image from GCS: {e}]"


        # Build the review prompt
        user_message = f"""
Original "audience_profile":
{audience_analysis}

Original "strategy_summary":
{content_strategy}

Original "marketing_copy":
{marketing_copy}

Original "design_recommendations":
{design_suggestion}

Original "image_generation_result":
{image_path_display}
{image_review_text}

### EXAMPLE OUTPUT FORMAT ###

**Original "audience_profile":**

**Original "audience_profile" score:**

**Modified "audience_profile":**

**Suggestion:**

<br><br>

**Original "strategy_summary":**

**Original "strategy_summary" score:**

**Modified "strategy_summary":**

**Suggestion:**

<br><br><br>

**Original "marketing_copy":**

**Original "marketing_copy" score:**

**Modified "marketing_copy":**

**Suggestion:**

<br><br><br>

**Original "design_recommendations":**

**Original "design_recommendations" score:**

**Modified "design_recommendations":**

**Suggestion:**

<br><br><br>

**Original "image_generation_result":**

**Original "image_generation_result" score:**

**Suggestion:**
"""
        print(f"[{self.name}] Reviewing full content with image embed...")
        try:
            review_output = self.call_llm(system_prompt=self.instruction, user_message=user_message)
            print(f"[{self.name}] Review complete.")

            # Extract modified strategy and copy
            modified_parts = self.extract_modified_components(review_output)

            # Save to session if tool_context is provided
            if tool_context:
                if "strategy_summary" in modified_parts:
                    tool_context.session.set("final_strategy", modified_parts["strategy_summary"])
                if "marketing_copy" in modified_parts:
                    tool_context.session.set("final_copy", modified_parts["marketing_copy"])

            return review_output
        except Exception as e:
            return f"Error: Review failed: {e}"
   
# Instantiate
reviewer_agent = ReviewerAgent()
