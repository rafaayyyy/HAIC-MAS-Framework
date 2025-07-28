import os
from datetime import datetime
from agents import function_tool



@function_tool
def get_human_input(agent_name: str, prompt: str) -> str:
    """Prompt the human user via CLI and return their response."""
    print(f"\n[HUMAN INPUT NEEDED - {agent_name}] {prompt}")
    return input("Your response: ")

@function_tool
def get_human_input_from_file(agent_name: str, prompt: str) -> str:
    """Prompts the human to write input to a file and reads the response.
    
    Args:
        agent_name: The name of the agent that is prompting the human for input.
        prompt: The message to display to the human user.
    Returns:
        The content of the file written by the human.
    """
    print(f"Human input required - {agent_name}:\n {prompt}")
    
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

        file_location = os.path.join(run_dir, f"humans_input_{next_run}.txt")

        # Clear the file first (create empty file or overwrite existing content)
        with open(file_location, "w") as f:
            f.write("")  # Clear the file
            
        print(f"Please write your response to '{file_location}' and type 'Done' when finished.")
        
    except Exception as e:
        print(f"ERROR: Could not setup human input file - {str(e)}")
        return f"ERROR: Could not setup human input file - {str(e)}"
    
    # Wait for user to type "Done"
    while True:
        user_input = input("Type 'Done' when you have finished writing to the file: ")
        if user_input.strip().lower() == "done":
            break
        else:
            print("Please type 'Done' when you have finished writing to the file.")
    
    # Read the file content
    try:
        with open(file_location, "r") as f:
            content = f.read().strip()
            
        # Clean up - delete the file after reading
        try:
            os.remove(file_location)
        except:
            pass  # Don't fail if we can't delete the file
            
        return content
    except FileNotFoundError:
        return f"ERROR: {file_location} file not found. Please create the file and write your response."
    except Exception as e:
        return f"ERROR: Could not read file - {str(e)}"
