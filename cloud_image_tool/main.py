import vertexai
import io
import tempfile
import uuid
from PIL import Image as PIL_Image

# Imports for the cloud-native tool
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.language_models._language_models import save_artifact

# --- Configuration ---
# The cloud environment will use the project it's running in.
# Initializing is still good practice.
vertexai.init()

IMAGE_MODEL = "imagen-3.0" # Or your preferred model

def generate_image_from_upload(
    prompt: str,
    product_image_gcs_uri: str
) -> dict:
    """
    Generates an image from a prompt and an uploaded product image, saving the
    result to the agent's artifact panel.

    Args:
        prompt: The text description of the desired image.
        product_image_gcs_uri: The GCS URI of the user's uploaded product image,
                               provided automatically by the web UI.

    Returns:
        A dictionary with the status and detail of the operation.
    """
    print(f"Starting image generation with prompt: '{prompt[:75]}...'")
    print(f"Using user-uploaded image from: {product_image_gcs_uri}")

    try:
        # 1. Load the user's uploaded image from the GCS URI
        user_uploaded_image = Part.from_uri(
            mime_type="image/png",  # The UI should handle various types
            uri=product_image_gcs_uri
        )

        # 2. Call the model with both the text prompt and the uploaded image
        model = GenerativeModel(IMAGE_MODEL)
        response = model.generate_content([
            user_uploaded_image,
            f"Using the provided product image, create a new image based on this request: {prompt}"
        ])

        if not response.candidates or not response.candidates[0].content.parts:
            return {"status": "failed", "detail": "Image generation returned no content."}

        # 3. Save the generated image to the Artifacts panel
        image_bytes = response.candidates[0].content.parts[0].data
        filename = f"generated_image_{uuid.uuid4().hex}.png"

        # The save_artifact function requires a local file path, so we use a temp file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_file.write(image_bytes)
            artifact_uri = save_artifact(artifact_id=filename, file_path=temp_file.name)

        print(f"Image saved to artifact panel: {artifact_uri}")

        return {
            "status": "success",
            "detail": f"I've created the image and it's available in the artifacts panel.",
            "filename": filename
        }

    except Exception as e:
        print(f"ERROR during image generation: {e}")
        return {"status": "failed", "detail": f"An error occurred: {e}"}