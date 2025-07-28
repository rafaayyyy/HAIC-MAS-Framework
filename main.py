import asyncio
from agents import Runner
from agents_impl.path_generation_agent import path_generation_agent
from agents_impl.orchestrator_agent import orchestrator
from utils.format_output import format_pydantic_output
from data.toassess import toassess
from human_agents_impl.orchestrator_human_agents import orchestrator_human_agents

blog = f"""

Analyse the following scenario ethically, legally, ui/ux and technically and provide a summary of the content.

SCENARIO TO ANALYSE:

{toassess}

"""


async def main():
    result = await Runner.run(
        starting_agent=orchestrator_human_agents,
        input=blog,
        max_turns=50
    )
    final_output = getattr(result, "final_output", None)

    if final_output:
        print("\n" + "="*60)
        print("STRUCTURED OUTPUT RESULTS")
        print("="*60)
        
        # User-friendly formatted output
        formatted_output = format_pydantic_output(final_output)
        print(formatted_output)
    else:
        print("\n[!] No `final_output` found in the result.\n")

    return


    # Interactive loop - get input from user until they type 'proceed'
    while True:
        user_input = input("What path do you want to take or do you have any comments? (Type 'proceed' to continue to the next step i.e. Generate Recommendations)\nUser Input: ")
        new_input = result.to_input_list() + [{"role": "user", "content": user_input}]
        result = await Runner.run(path_generation_agent, new_input)
        # Extract and pretty-print only the final_output
        final_output = getattr(result, "final_output", None)

        if final_output:
            print("\n" + "="*60)
            print("STRUCTURED OUTPUT RESULTS")
            print("="*60)
            
            # User-friendly formatted output
            formatted_output = format_pydantic_output(final_output)
            print(formatted_output)
        else:
            print("\n[!] No `final_output` found in the result.\n")
        if user_input.lower() == 'proceed':
            break

    print("\n\n\nZ-Inspection complete")

if __name__ == "__main__":
    asyncio.run(main())