"""image_generator_agent: An agent for creating images from a prompt."""

import os
import traceback
from pathlib import Path
import io
import webbrowser

# --- Imports for Image Display ---
import IPython.display
from PIL import Image as PIL_Image
from PIL import ImageOps as PIL_ImageOps

from dotenv import load_dotenv

# --- Core ADK and GenAI Imports ---
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk import Runner
from google.adk.tools import ToolContext
from google.genai import Client, types

# --- Configuration ---
load_dotenv()

# Models
REASONING_MODEL = "gemini-1.5-pro-latest"
IMAGE_MODEL = "imagen-4.0-generate-preview-05-20"

# Local storage path for images
LOCAL_IMAGE_DIR = "generated_images"
os.makedirs(LOCAL_IMAGE_DIR, exist_ok=True)

# --- Client Initialization ---
try:
    client = Client(
        vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    )
    print("✅ Vertex AI client initialized successfully using google.genai.Client.")
except Exception as e:
    print(f"ERROR: Could not initialize Vertex AI client: {e}")
    client = None

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
    Generates an image from a prompt, saves it, and displays it.
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

        image_bytes = response.generated_images[0].image.image_bytes
        filename = f"generated_image_{invocation_id[:8]}.png"
        local_path = Path(LOCAL_IMAGE_DIR) / filename

        pil_image = PIL_Image.open(io.BytesIO(image_bytes))
        pil_image.save(local_path)
        print(f"[{tool_context.agent_name}] Image saved locally at: {local_path}")

        tool_context.save_artifact(
            filename,
            types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
        )

        if is_in_notebook():
            display_image(pil_image)
        else:
            webbrowser.open(local_path.resolve().as_uri())

        return {
            "status": "success",
            "detail": f"I've created an image and saved it as {filename}",
            "filename": filename
        }

    except Exception as e:
        traceback.print_exc()
        return {"status": "failed", "detail": f"Error during image generation: {type(e).__name__}: {e}"}

# Agent definition
image_generator_agent = Agent(
    name="image_generator_agent",
    model=REASONING_MODEL,
    description="An agent that generates images from text descriptions.",
    instruction=(
        "You are an Image Generation Agent. Take the user's request, "
        "refine it into a detailed descriptive prompt, and use the "
        "`generate_image` tool. Report back on the status."
    ),
    tools=[generate_image],
)

# Runner to test the agent
if __name__ == "__main__":
    if is_in_notebook():
         print("⚠️ Running in a notebook. The interactive command-line loop is disabled.")
         print("   To test, call Runner.run() in a new cell, e.g.:")
         print("   Runner.run(agent=image_generator_agent, prompt='a cat on a skateboard')")
    else:
        artifact_service = InMemoryArtifactService()
        print("\n--- Starting Image Generation Agent ---")
        print("Enter a prompt to generate an image, or 'quit' to exit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                break

            response_generator = Runner.run(
                agent=image_generator_agent,
                prompt=user_input,
                artifact_service=artifact_service,
            )
   
            for chunk in response_generator:
                if "text" in chunk:
                    print(f"Agent: {chunk['text']}", end="", flush=True)
            print()