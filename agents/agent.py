from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from . import prompt 
from .subagents.audience_analyst_agent import audience_analyst_agent
#from .subagents.content_strategist_agent import content_strategist_agent
from .subagents.copywriter_agent import copywriter_agent
from .subagents.formatter_agent import formatter_agent
#from .subagents.reviewer_agent import reviewer_agent
#from .subagents.scheduler_agent import scheduler_agent

MODEL = "gemini-2.5-pro-preview-05-06"

contentgenie_orchestrator = Agent(
    name="contentgenie_orchestrator",
    model=MODEL,
    description="An AI-powered content generation and marketing automation agent.",
    instruction=prompt.ORCHESTRATOR_PROMPT,
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
