from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt 
from .sub_agents.audience_analyst import audience_analyst_agent
from .sub_agents.content_strategist import content_strategist_agent
from .sub_agents.copywriter import copywriter_agent
from .sub_agents.formatter import formatter_agent
from .sub_agents.reviewer import reviewer_agent
from .sub_agents.scheduler import scheduler_agent

MODEL = "gemini-2.5-pro-preview-05-06"

contentgenie_orchestrator = LlmAgent(
    name="contentgenie_orchestrator",
    model=MODEL,
    description="An AI-powered content generation and marketing automation agent.",
    instruction=prompt.ORCHESTRATOR_PROMPT,
    tools=[
        AgentTool(agent=audience_analyst_agent),
        AgentTool(agent=content_strategist_agent),
        AgentTool(agent=copywriter_agent),
        AgentTool(agent=formatter_agent),
        AgentTool(agent=reviewer_agent),
        AgentTool(agent=scheduler_agent),
    ]
)

root_agent = contentgenie_orchestrator
