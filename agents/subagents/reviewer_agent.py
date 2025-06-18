import os
import io
from agents.base_agent import BaseAgent
from PIL import Image
from google.cloud import storage
import google.generativeai as genai

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
original "Audience Analysis":
{audience_analysis}

original "Content Strategy":
{content_strategy}

original "Marketing Copy":
{marketing_copy}

original "Design Suggestion":
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
