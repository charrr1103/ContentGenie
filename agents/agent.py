
import os
import asyncio
from google.adk.agents import Agent, LlmAgent # Ensure LlmAgent is imported
from google.adk.models.lite_llm import LiteLlm # For multi-model support (if used directly)
from google.adk.sessions import InMemorySessionService # No longer directly used here, but good to keep if needed elsewhere
from google.adk.runners import Runner # No longer directly used here
from google.genai import types # For creating message Content/Parts (if used directly)

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

print("Libraries imported.")

from . import prompt
from .subagents.audience_analyst_agent import audience_analyst_agent
#from .subagents.content_strategist_agent import content_strategist_agent
from .subagents.copywriter_agent import copywriter_agent
from .subagents.formatter_agent import formatter_agent
#from .subagents.reviewer_agent import reviewer_agent
#from .subagents.scheduler_agent import scheduler_agent

# Import BaseAgent and use it consistently
from .base_agent import BaseAgent

MODEL = "gemini-2.5-pro-preview-05-06"

<<<<<<< HEAD

=======
>>>>>>> deb16e3a7677778a407506fe71e68c6ee550483f
# Define the Orchestrator using your BaseAgent (which is an LlmAgent)
contentgenie_orchestrator = BaseAgent

contentgenie_orchestrator = Agent(
<<<<<<< HEAD

=======
>>>>>>> deb16e3a7677778a407506fe71e68c6ee550483f
    name="contentgenie_orchestrator",
    model=MODEL, # This is correct for LlmAgent
    description="An AI-powered content generation and marketing automation agent.",
    instruction=prompt.ORCHESTRATOR_PROMPT, # Use instruction for the prompt
    tools=[
        AgentTool(agent=audience_analyst_agent),
        #AgentTool(agent=content_strategist_agent),
        AgentTool(agent=copywriter_agent),
        AgentTool(agent=formatter_agent),
        #AgentTool(agent=reviewer_agent),
        #AgentTool(agent=scheduler_agent),
    ]
)

root_agent = contentgenie_orchestrator