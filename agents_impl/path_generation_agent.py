from agents import Agent, Runner, function_tool, handoff, AgentOutputSchema, ModelSettings, RunContextWrapper
import asyncio
import sys
import os
from agents import Runner
from agents.extensions import handoff_filters
from agents import Agent, handoff, AgentOutputSchema

# Add the parent directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.configs import system_llm, PIPELINE_MODEL, PIPELINE_TEMPERATURE
from agents_impl.internal_docs_agent import internal_docs_agent
from agents_impl.recommendation_agent import recommendation_agent
from utils.format_output import format_pydantic_output
from prompts.path_generation_agent_prompt import PATH_GENERATION_AGENT_PROMPT
from schemas.path_generation_schemas import PathOption, StrategicGuidance, PathGenerationResult
from utils.save_agent_output import save_generated_paths
from utils.save_agent_output import agents_append_output_tool


internal_docs_tool = internal_docs_agent.as_tool(
    tool_name="internal_docs",
    tool_description="Call this Z-Inspection documentation assistant to get information about: (1) The Z-Inspection methodology and process steps from setup_phase.md, (2) Details about the system being analyzed from system_being_analyzed.md. This agent helps other agents understand the Z-Inspection process, their role in the project, and provides context about the system under evaluation. It can restructure queries and search across multiple project documents."
)


@function_tool
def get_orchestrator_workflow_output():
    """
    Get the latest run number from configs/runs.txt and read the orchestrator workflow JSON file:
    z_inspection_workflow_*.json from the latest run folder
    """
    import json
    import glob
    
    try:
        runs_file_path = "configs/runs.txt"
        
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    # Get latest run number (last line)
                    latest_run = int(lines[-1].strip())
                else:
                    return {"error": "No runs found in runs.txt"}
        else:
            return {"error": "runs.txt file not found"}
        
        # Construct the folder path
        folder_path = f"z_inspection_logs/mas_run_{latest_run}"
        
        if not os.path.exists(folder_path):
            return {"error": f"Folder {folder_path} not found"}
        
        # Find orchestrator workflow JSON file with timestamp pattern
        orchestrator_pattern = os.path.join(folder_path, "z_inspection_workflow_*.json")
        
        # Read orchestrator workflow output
        orchestrator_files = glob.glob(orchestrator_pattern)
        if orchestrator_files:
            # Use the most recent one if multiple exist
            orchestrator_file = max(orchestrator_files, key=os.path.getctime)
            with open(orchestrator_file, 'r') as f:
                workflow_data = json.load(f)
                print("Read orchestrator workflow data")
                return {"orchestrator_workflow": workflow_data}
        else:
            return {"error": "z_inspection_workflow_*.json not found"}
        
    except Exception as e:
        return {"error": f"Failed to read workflow file: {str(e)}"}

@function_tool
def save_output_tool(output_data: str):
    f"""Send the output data to the save_generated_paths function to save the paths. Send the output data as a JSON string with structured output of {PathGenerationResult.__name__}.
    
    Args:
        output_data (str): The output data to save as JSON string.

    Returns:
        str: The response from the save_generated_paths function.
    """
    return save_generated_paths(output_data)

# Enhanced on_handoff function to save complete workflow
async def on_handoff(ctx: RunContextWrapper[None]):
    print("🔄 Generating final Recommendations")

# we then pass this function to the handoff object
recommendation_handoff = handoff(agent=recommendation_agent, on_handoff=on_handoff, input_filter=handoff_filters.remove_all_tools)

path_generation_agent = Agent(
    name="Path Generation Agent",
    model=PIPELINE_MODEL,
    model_settings=ModelSettings(
                temperature=PIPELINE_TEMPERATURE,
                tool_choice="required",
            ),
    instructions=PATH_GENERATION_AGENT_PROMPT,
    tools=[get_orchestrator_workflow_output, internal_docs_tool, save_output_tool],
    handoffs=[recommendation_handoff],
    handoff_description="Handoff to the Recommendation Agent after generating the paths and getting the human's collective feedback. Once the user types 'Proceed' in the console, handoff to the Recommendation Agent.",
    output_type=AgentOutputSchema(
                PathGenerationResult,
                strict_json_schema=False,
            )
)