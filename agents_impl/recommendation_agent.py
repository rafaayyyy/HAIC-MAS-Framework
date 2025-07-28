from agents import Agent, Runner, function_tool, AgentOutputSchema, ModelSettings
import os
import asyncio
import sys
# Add the parent directory to the Python path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.configs import system_llm, PIPELINE_MODEL, PIPELINE_TEMPERATURE
from utils.format_output import format_pydantic_output
from prompts.recommendation_agent_prompt import RECOMMENDATION_AGENT_PROMPT
from schemas.recommendation_schemas import RecommendationResult
from utils.save_agent_output import save_recommendations
from utils.save_agent_output import agents_append_output_tool
from agents_impl.internal_docs_agent import internal_docs_agent

internal_docs_tool = internal_docs_agent.as_tool(
    tool_name="internal_docs",
    tool_description="Call this Z-Inspection documentation assistant to get information about: (1) The Z-Inspection methodology and process steps from setup_phase.md, (2) Details about the system being analyzed from system_being_analyzed.md. This agent helps other agents understand the Z-Inspection process, their role in the project, and provides context about the system under evaluation. It can restructure queries and search across multiple project documents."
)


@function_tool
def get_orchestrator_and_path_generation_agent_output():
    """
    Get the second last number from configs/runs.txt and read both JSON files:
    1. Orchestrator workflow output (z_inspection_workflow_*.json)
    2. Path generation agent output (generated_paths_*.json)
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
        
        # Find JSON files with timestamp patterns
        orchestrator_pattern = os.path.join(folder_path, "z_inspection_workflow_*.json")
        path_generation_pattern = os.path.join(folder_path, "generated_paths_*.json")
        
        result = {}
        
        # Read orchestrator workflow output
        orchestrator_files = glob.glob(orchestrator_pattern)
        if orchestrator_files:
            # Use the most recent one if multiple exist
            orchestrator_file = max(orchestrator_files, key=os.path.getctime)
            with open(orchestrator_file, 'r') as f:
                print("Read orchestrator workflow data")
                result["orchestrator_workflow"] = json.load(f)
        else:
            print("Orchestrator workflow data not found")
            result["orchestrator_workflow"] = {"error": "z_inspection_workflow_*.json not found"}
        
        # Read path generation agent output
        path_generation_files = glob.glob(path_generation_pattern)
        if path_generation_files:
            # Use the most recent one if multiple exist
            path_generation_file = max(path_generation_files, key=os.path.getctime)
            with open(path_generation_file, 'r') as f:
                print("Read path generation workflow data")
                result["path_generation_workflow"] = json.load(f)
        else:
            print("Path generation workflow data not found")
            result["path_generation_workflow"] = {"error": "generated_paths_*.json not found"}
        return result
        
    except Exception as e:
        return {"error": f"Failed to read files: {str(e)}"}


@function_tool
def save_output_tool(output_data: str):
    f"""Send the output data to the save_recommendations function to save the recommendations. Send the output data as a JSON string with structured output of {RecommendationResult.__name__}.
    
    Args:
        output_data (str): The output data to save as JSON string.

    Returns:
        str: The response from the save_recommendations function.
    """
    return save_recommendations(output_data)


recommendation_agent = Agent(
    name="Z-Inspection Recommendation Agent",
    model=PIPELINE_MODEL,
    model_settings=ModelSettings(
                temperature=PIPELINE_TEMPERATURE,
                tool_choice="required",
            ),
    instructions=RECOMMENDATION_AGENT_PROMPT,
    tools=[get_orchestrator_and_path_generation_agent_output, internal_docs_tool, save_output_tool],
    output_type=AgentOutputSchema(
        RecommendationResult,
        strict_json_schema=False,
    ),
)