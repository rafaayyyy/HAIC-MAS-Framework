from agents import Agent, function_tool, ModelSettings
from .internal_docs_agent import internal_docs_agent
from utils.save_agent_output import save_agent_output
from prompts.linguistic_expert_agent_prompt import LINGUISTIC_EXPERT_AGENT_PROMPT
from configs.configs import DOMAIN_EXPERT_MODEL, DOMAIN_EXPERT_TEMPERATURE
from utils.save_agent_output import agents_append_output_tool

internal_docs_tool = internal_docs_agent.as_tool(
    tool_name="internal_docs",
    tool_description="Call this Z-Inspection documentation assistant to get information about: (1) The Z-Inspection methodology and process steps from setup_phase.md, (2) Details about the system being analyzed from system_being_analyzed.md. This agent helps other agents understand the Z-Inspection process, their role in the project, and provides context about the system under evaluation. It can restructure queries and search across multiple project documents."
)

@function_tool
def save_output_tool(output_data: str):
    """Save this agent's output to the agents_outputs folder."""
    return save_agent_output("linguistic_expert_agent", output_data)

linguistic_expert_agent = Agent(
    name="Linguistic Expert Agent",
    model=DOMAIN_EXPERT_MODEL,
    model_settings=ModelSettings(
                temperature=DOMAIN_EXPERT_TEMPERATURE,
                tool_choice="required",
            ),
    instructions=LINGUISTIC_EXPERT_AGENT_PROMPT,
    tools=[internal_docs_tool, save_output_tool, agents_append_output_tool],
)