from agents import Agent, function_tool, ModelSettings
from .internal_docs_agent import internal_docs_agent

import sys
import os

# Add the parent directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents_impl.islamic_content_verification_agent import islamic_verification_Custom
from prompts.islamic_ethical_agent_prompt import ISLAMIC_ETHICAL_AGENT_PROMPT
from configs.configs import DOMAIN_EXPERT_MODEL, DOMAIN_EXPERT_TEMPERATURE
from utils.save_agent_output import save_agent_output
from utils.save_agent_output import agents_append_output_tool

internal_docs_tool = internal_docs_agent.as_tool(
    tool_name="internal_docs",
    tool_description="Call this Z-Inspection documentation assistant to get information about: (1) The Z-Inspection methodology and process steps from setup_phase.md, (2) Details about the system being analyzed from system_being_analyzed.md. This agent helps other agents understand the Z-Inspection process, their role in the project, and provides context about the system under evaluation. It can restructure queries and search across multiple project documents."
)

# islamic_content_verification_tool = islamic_content_verification_agent.as_tool(
#     tool_name="islamic_content_verification",
#     tool_description="Call this Islamic content verification expert to authenticate and validate Islamic references. Use this tool to verify hadith citations and their authenticity, Quranic verses and their translations, scholarly sources and their credibility, and URLs claiming Islamic authority. When calling this tool, specify exactly what you want verified"
# )



@function_tool
def save_output_tool(output_data: str):
    """Save this agent's output to the agents_outputs folder."""
    return save_agent_output("islamic_ethical_agent", output_data)

islamic_ethical_agent = Agent(
    name="Islamic Ethical Agent",
    model=DOMAIN_EXPERT_MODEL,
    model_settings=ModelSettings(
                temperature=DOMAIN_EXPERT_TEMPERATURE,
                tool_choice="required",
            ),
    instructions=ISLAMIC_ETHICAL_AGENT_PROMPT,
    tools=[islamic_verification_Custom, internal_docs_tool, save_output_tool, agents_append_output_tool],
)