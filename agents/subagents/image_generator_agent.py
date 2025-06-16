import os
import traceback
from pathlib import Path
import io

# --- Imports for Image Display ---
import IPython.display
from PIL import Image as PIL_Image

from dotenv import load_dotenv

# --- Core ADK and GenAI Imports ---
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk import Runner
from google.adk.tools import ToolContext
from google.genai import Client, types

# --- GCS Import ---
from google.cloud import storage

# --- Configuration ---
load_dotenv()

# Models
REASONING_MODEL = "gemini-1.5-pro-latest"
IMAGE_MODEL = "imagen-3.0-generate-002" # This model is for text-to-image generation.

# Local storage path (still useful for local viewing/debugging)
LOCAL_IMAGE_DIR = "generated_images"
os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)

# --- GCS Configuration ---
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

# --- Client Initialization ---
try:
    # GenAI Client
    client = Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )
    print("✅ Vertex AI client initialized successfully using google.genai.Client.")

    # GCS Client
    if GCS_BUCKET_NAME:
        storage_client = storage.Client()
        print("✅ Google Cloud Storage client initialized successfully.")
    else:
        storage_client = None
        print("⚠️ GCS_BUCKET_NAME not set. GCS upload will be skipped.")

except Exception as e:
    print(f"ERROR: Could not initialize clients: {e}")
    client = None
    storage_client = None


def is_in_notebook() -> bool:
    """Checks if the code is running in a notebook environment."""
    try:
        return get_ipython().__class__.__name__ == 'ZMQInteractiveShell'  # type: ignore
    except NameError:
        return False

def display_image(pil_image: PIL_Image.Image) -> None:
    """Displays a PIL image in a notebook with default size."""
    if pil_image.mode != "RGB":
        pil_image = pil_image.convert("RGB")
    IPython.display.display(pil_image)

def generate_image(
    tool_context: ToolContext,
    *,
    prompt: str,
) -> dict:
    """
    Generates an image from a text prompt, uploads it to GCS, saves it to the ADK UI,
    and returns the GCS path.
    """
    if not client:
        return {"status": "Failed", "detail": "Vertex AI Client not initialized."}

    invocation_id = tool_context.invocation_id
    print(f"[{tool_context.agent_name}] Generating image with prompt: '{prompt[:75]}...'")

    try:
        response = client.models.generate_images(
            model=IMAGE_MODEL,
            prompt=prompt,
        )

        if not response.generated_images:
            return {"status": "failed", "detail": "Image generation returned no images."}

        # --- Image Data ---
        image_bytes = response.generated_images[0].image.image_bytes
        filename = f"generated_image_{invocation_id[:8]}.png"
        pil_image = PIL_Image.open(io.BytesIO(image_bytes))

        # --- 1. Upload to Google Cloud Storage (if configured) ---
        gcs_uri = None
        gcs_error = None # Variable to hold a potential error message
        if storage_client and GCS_BUCKET_NAME:
            try:
                bucket = storage_client.bucket(GCS_BUCKET_NAME)
                blob = bucket.blob(filename)
                blob.upload_from_string(image_bytes, content_type="image/png")
                gcs_uri = f"gs://{GCS_BUCKET_NAME}/{filename}"
                print(f"[{tool_context.agent_name}] Image uploaded to GCS at: {gcs_uri}")
            except Exception as e:
                # Don't return. Just log the error and continue.
                gcs_error = str(e)
                print(f"ERROR: Failed to upload to GCS: {gcs_error}")
        
        # --- 2. Save artifact to ADK Web UI ---
        # This part will now be reached even if GCS upload fails.
        tool_context.save_artifact(
            filename,
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        )
        print(f"[{tool_context.agent_name}] Artifact saved to ADK UI panel.")

        # --- 3. Handle local display/saving ---
        if is_in_notebook():
            display_image(pil_image)
        else:
            local_path = Path(LOCAL_IMAGE_DIR) / filename
            pil_image.save(local_path)
            print(f"[{tool_context.agent_name}] Image saved locally at: {local_path}")

        # --- 4. Return a detailed result with the GCS path ---
        detail_message = f"I've created an image and saved it to the ADK UI. "
        if gcs_uri:
            detail_message += f"It is also available at {gcs_uri}."
        elif gcs_error:
            detail_message += f"The upload to GCS failed: {gcs_error}"

        return {
            "status": "success",
            "detail": detail_message,
            "filename": filename,
            "gcs_uri": gcs_uri
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "detail": f"Error during image generation: {type(e).__name__}: {e}"}

# Agent definition
image_generator_agent = Agent( # Renamed for clarity
    name="image_generator_agent",
    model=REASONING_MODEL,
    description="An agent that generates images from text descriptions and saves them to Google Cloud Storage.",
    instruction=(
        "You are an Image Generation Agent. Your primary function is to create images based on text descriptions. "
        "When a user provides a textual prompt, call the `generate_image` tool with that prompt. "
        "Report back on the status, including the final GCS path of the image if available."
    ),
    tools=[generate_image],
)

# Runner to test the agent
if __name__ == "__main__":
    if is_in_notebook():
        print("⚠️ Running in a notebook. The interactive command-line loop is disabled.")
        print("   To test, call Runner.run() in a new cell, e.g.:")
        print("   Runner.run(agent=content_generator_agent, prompt='a photorealistic painting of a robot artist in a Parisian studio')")
    else:
        # Check if GCS is configured for the local run
        if not GCS_BUCKET_NAME:
            print("\nWARNING: GCS_BUCKET_NAME is not set in your .env file. Images will not be uploaded to GCS during this local run.")
            
        artifact_service = InMemoryArtifactService()
        print("\n--- Starting Content Generation Agent ---")
        print("Enter a text prompt to generate an image, or 'quit' to exit.")
        while True:
            user_input = input("You (text prompt): ")
            if user_input.lower() == "quit":
                break

            response_generator = Runner.run(
                agent=image_generator_agent,
                prompt=user_input, # Agent is configured to take a text prompt for image generation
                artifact_service=artifact_service,
            )
        
            for chunk in response_generator:
                if "text" in chunk:
                    print(f"Agent: {chunk['text']}", end="", flush=True)
            print()