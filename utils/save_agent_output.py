import os
import json
from datetime import datetime
from agents import function_tool

def save_agent_output(agent_name: str, output_data: str):
    """
    Save agent output to a file in the agents_outputs folder under the current run directory.
    
    Args:
        agent_name: Name of the agent (e.g., "ethical_agent", "legal_agent", "islamic_ethical_agent", "linguistic_expert_agent")
        output_data: The output string from the agent
    
    Returns:
        'DONE' on success or error message on failure.
    """
    try:
        # Read the current run number from configs/runs.txt
        runs_file_path = "configs/runs.txt"
        
        # Ensure configs directory exists
        os.makedirs("configs", exist_ok=True)
        
        # Read current run number
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    current_run = int(lines[-1].strip())
                else:
                    current_run = 0
        else:
            current_run = 0
        
        # Increment run number for new workflow
        next_run = current_run + 1
        
        # Create agents_outputs directory in base directory
        agents_outputs_dir = "agents_outputs"
        os.makedirs(agents_outputs_dir, exist_ok=True)
        
        # Create run-specific directory inside agents_outputs using next run number
        run_dir = os.path.join(agents_outputs_dir, f"mas_run_{next_run}")
        os.makedirs(run_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{agent_name}_{timestamp}.txt"
        filepath = os.path.join(run_dir, filename)

        # Escape the output data using json.dumps
        escaped_text = json.dumps(output_data)
        
        # Save the escaped output data to text file
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(escaped_text)
            
        print(f"✅ {agent_name} output saved to: {filepath}")
        
        return "DONE"
        
    except Exception as e:
        error_msg = f"Error saving {agent_name} output: {str(e)}"
        print(f"❌ {error_msg}")
        return f"ERROR: {error_msg}" 
    


def save_workflow(workflow_data: str) -> str: 
    """
    Save the Z-Inspection workflow to a JSON file in a dedicated folder. Pass the ZInspectionWorkflow object as JSON string.
    This function is called when orchestrator agent calls this tool.
    Returns 'DONE' on success or error message on failure.
    """
    try:
        # Read the current run number from configs/runs.txt
        runs_file_path = "configs/runs.txt"
        
        # Ensure configs directory exists
        os.makedirs("configs", exist_ok=True)
        
        # Read current run number
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    current_run = int(lines[-1].strip())
                else:
                    current_run = 0
        else:
            current_run = 0
        
        # Increment run number
        next_run = current_run + 1
        
        # Create z_inspection_logs directory if it doesn't exist
        logs_dir = "z_inspection_logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create run-specific directory inside z_inspection_logs
        run_dir = os.path.join(logs_dir, f"mas_run_{next_run}")
        os.makedirs(run_dir, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"z_inspection_workflow_{timestamp}.json"
        filepath = os.path.join(run_dir, filename)
        
        # Parse JSON string to dictionary
        try:
            workflow_dict = json.loads(workflow_data)
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error: {str(e)}"
            print(f"⚠️ {error_msg}")
            print(f"🔍 Raw input received: {workflow_data[:200]}...")
            return f"ERROR: {error_msg}. Please fix the JSON format and try again."
        
        # Save the data to JSON file
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(workflow_dict, f, indent=2, ensure_ascii=False)
        
        # Update runs.txt with the new run number
        with open(runs_file_path, "a") as f:
            f.write(f"\n{next_run}")
            
        print(f"✅ Z-Inspection workflow saved to: {filepath}")
        print(f"📁 Run directory created: {run_dir}")
        print(f"🔢 Run number updated: {next_run}")
        
        return "DONE"
        
    except Exception as e:
        error_msg = f"Error saving Z-Inspection workflow: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"🔍 Input data type: {type(workflow_data)}")
        return f"ERROR: {error_msg}. Please check your data format and try again."


def save_generated_paths(generated_paths: str) -> str: 
    """
    Save the generated paths to a JSON file in a dedicated folder. Pass the PathGenerationResult object as JSON string.
    This function is called when path generation agent calls this tool.
    Returns 'DONE' on success or error message on failure.
    """
    try:
        # Read the current run number from configs/runs.txt to find the latest run folder
        runs_file_path = "configs/runs.txt"
        
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    current_run = int(lines[-1].strip())
                else:
                    current_run = 1
        else:
            current_run = 1
        
        # Locate the most recent run directory
        logs_dir = "z_inspection_logs"
        run_dir = os.path.join(logs_dir, f"mas_run_{current_run}")
        
        # Generate unique filename with timestamp for paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_paths_{timestamp}.json"
        filepath = os.path.join(run_dir, filename)
        
        # Parse JSON string to dictionary
        try:
            paths_dict = json.loads(generated_paths)
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error: {str(e)}"
            print(f"⚠️ {error_msg}")
            print(f"🔍 Raw input received: {generated_paths[:200]}...")
            return f"ERROR: {error_msg}. Please fix the JSON format and try again."
        
        # Save the data to JSON file
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(paths_dict, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Generated paths saved to: {filepath}")
        print(f"📁 Saved in run directory: {run_dir}")
        
        return "DONE"
        
    except Exception as e:
        error_msg = f"Error saving generated paths: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"🔍 Input data type: {type(generated_paths)}")
        return f"ERROR: {error_msg}. Please check your data format and try again."

def save_recommendations(recommendations_data: str) -> str: 
    """
    Save the recommendations to a JSON file in a dedicated folder. Pass the recommendation agent's output as JSON string.
    This function is called when recommendation agent calls this tool.
    Returns 'DONE' on success or error message on failure.
    """
    try:
        # Read the current run number from configs/runs.txt to find the latest run folder
        runs_file_path = "configs/runs.txt"
        
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    current_run = int(lines[-1].strip())
                else:
                    current_run = 1
        else:
            current_run = 1
        
        # Locate the most recent run directory
        logs_dir = "z_inspection_logs"
        run_dir = os.path.join(logs_dir, f"mas_run_{current_run}")
        
        # Generate unique filename with timestamp for recommendations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recommendations_{timestamp}.json"
        filepath = os.path.join(run_dir, filename)
        
        # Parse JSON string to dictionary
        try:
            recommendations_dict = json.loads(recommendations_data)
        except json.JSONDecodeError as e:
            error_msg = f"JSON parsing error: {str(e)}"
            print(f"⚠️ {error_msg}")
            print(f"🔍 Raw input received: {recommendations_data[:200]}...")
            return f"ERROR: {error_msg}. Please fix the JSON format and try again."
        
        # Save the data to JSON file
        with open(filepath, "w", encoding='utf-8') as f:
            json.dump(recommendations_dict, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Recommendations saved to: {filepath}")
        print(f"📁 Saved in run directory: {run_dir}")
        
        return "DONE"
        
    except Exception as e:
        error_msg = f"Error saving recommendations: {str(e)}"
        print(f"❌ {error_msg}")
        print(f"🔍 Input data type: {type(recommendations_data)}")
        return f"ERROR: {error_msg}. Please check your data format and try again."


@function_tool
def agents_append_output_tool(agent_name: str, output_data: str):
    """
    Save agent output to a file in append mode.
    
    Args:
        agent_name: Name of the agent (e.g., "orchestrator_agent", "designer_agent", "reviewer_agent", "linguistic_analyst_agent")
        output_data: The output string from the agent
    
    Returns:
        'DONE' on success or error message on failure.
    """
    try:
        # Read the current run number from configs/runs.txt
        runs_file_path = "configs/runs.txt"
        
        # Ensure configs directory exists
        os.makedirs("configs", exist_ok=True)
        
        # Read current run number
        if os.path.exists(runs_file_path):
            with open(runs_file_path, "r") as f:
                lines = f.readlines()
                if lines:
                    current_run = int(lines[-1].strip())
                else:
                    current_run = 0
        else:
            current_run = 0
        
        # Increment run number
        next_run = current_run + 1
        
        # Create z_inspection_logs directory if it doesn't exist
        logs_dir = "z_inspection_logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        # Create run-specific directory inside z_inspection_logs
        run_dir = os.path.join(logs_dir, f"mas_run_{next_run}")
        os.makedirs(run_dir, exist_ok=True)

        file_location = os.path.join(run_dir, f"pipeline_logs_{next_run}.txt")
        
        # Create the file if it doesn't exist
        if not os.path.exists(file_location):
            with open(file_location, 'w', encoding='utf-8') as f:
                f.write("")  # Create empty file
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format the output with separator and metadata
        formatted_output = f"""
{'='*80}
AGENT: {agent_name}
TIMESTAMP: {timestamp}
{'='*80}
{output_data}
{'='*80}

"""
        
        # Append to file
        with open(file_location, 'a', encoding='utf-8') as file:
            file.write(formatted_output)
        
        return "DONE"
        
    except Exception as e:
        print(f"ERROR: Failed to save output - {str(e)}")
        return f"ERROR: Failed to save output - {str(e)}"