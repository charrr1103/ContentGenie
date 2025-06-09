# C:\Users\Charmaine Hooi\ContentGenie-1\interfaces\demo_ui.py

import streamlit as st
import asyncio
from dotenv import load_dotenv
import os
import uuid # Import uuid for generating unique session IDs

# Import types from google.genai for structured input
from google.genai import types

# Set PYTHONIOENCODING for the Streamlit process to handle Unicode characters
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Ensure correct path for imports
from agents.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Load environment variables (e.g., for GOOGLE_API_KEY)
load_dotenv()

async def generate_content_from_agent(prod_desc: str, camp_goal: str) -> str:
    """
    Uses the ADK Runner to invoke the root_agent with combined input,
    passing required keyword arguments: user_id, session_id, and new_message,
    and ensuring the session is created.
    """
    # Initialize session service
    session_service = InMemorySessionService()

    # Define app_name (used consistently across Runner and Session creation)
    app_name = "ContentGenieApp"

    # Initialize Runner with required arguments: session_service, app_name, and agent
    runner = Runner(
        session_service=session_service,
        app_name=app_name, # Use the defined app_name
        agent=root_agent # The agent instance to be run
    )

    full_output_parts = []
    user_input_str = f"Product: {prod_desc}, Goal: {camp_goal}"

    # Generate unique IDs for user and session
    current_user_id = "streamlit_user_1" # Fixed user ID for this example
    current_session_id = str(uuid.uuid4()) # Unique session ID per interaction

    # IMPORTANT STEP: Create the session BEFORE calling runner.run_async()
    await session_service.create_session(
        app_name=app_name,
        user_id=current_user_id,
        session_id=current_session_id
    )

    # Prepare the new_message as a types.Content object
    new_message_content = types.Content(parts=[types.Part.from_text(text=user_input_str)])

    # Call runner.run_async with the required keyword arguments
    async for chunk in runner.run_async(
        user_id=current_user_id,
        session_id=current_session_id,
        new_message=new_message_content
    ):
        # Extract only the text content from the chunk
        if chunk.content and chunk.content.parts:
            for part in chunk.content.parts:
                if hasattr(part, 'text') and part.text: # Ensure 'text' attribute exists and is not empty
                    full_output_parts.append(str(part.text))
        # Optional: You might want to handle other types of chunks (e.g., tool calls) here if they appear
        # For now, we're focusing purely on the AI's text response.


    return "".join(full_output_parts)

st.set_page_config(page_title="ContentGenie AI", layout="centered")

st.title("✨ ContentGenie AI Marketing Assistant ✨")
st.markdown("Enter your product details and campaign goal to generate tailored marketing content!")

# Input fields
product_description = st.text_area(
    "Product Description:",
    placeholder="e.g., 'An AI-powered content generation and marketing automation platform that helps businesses create engaging content quickly.'",
    height=100
)
campaign_goal = st.text_area(
    "Campaign Goal:",
    placeholder="e.g., 'Increase brand awareness by 20% and drive 10% more leads in Q3.'",
    height=70
)

if st.button("Generate Content"):
    if not product_description or not campaign_goal:
        st.warning("Please fill in both the product description and campaign goal.")
    else:
        with st.spinner("Generating your marketing campaign... This might take a moment."):
            try:
                # Call the async helper function
                result = asyncio.run(generate_content_from_agent(product_description, campaign_goal))

                st.success("Content generation complete!")
                st.markdown("### Generated Campaign Plan:")
                st.write(result)

            except Exception as e:
                st.error(f"An error occurred during content generation: {e}")
                st.exception(e)
