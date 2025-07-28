from agents import Agent, ModelSettings, function_tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv
import requests
import json
from prompts.islamic_content_verification_agent_prompt import ISLAMIC_CONTENT_VERIFICATION_AGENT_PROMPT
from configs.configs import ISLAMIC_CONTENT_VERIFICATION_MODEL, ISLAMIC_CONTENT_VERIFICATION_TEMPERATURE, MAX_SEARCH_RESULTS, SEARCH_DEPTH
from agents import Runner

load_dotenv()


@function_tool
def fetch_quran_ayah(surah_num:int, ayah_num:int, translation:str='en.asad')->dict:
    """
    Fetch a specific Quran ayah by its surah number and ayah number.
    
    Args:
        surah_num (int): The number of the surah (e.g., 1 for Al-Fatihah)
        ayah_num (int): The number of the ayah within the surah
        translation (str): The translation to use (default: 'en.asad')
        
    Returns:
        dict: A dictionary containing:
            - surah (str): The name of the surah
            - translation (str): The translation of the surah
            - surah_number (int): The number of the surah
            - ayah_number (int): The number of the ayah
            - global_ayah (int): The global number of the ayah
            - text_arabic (str): The text of the ayah in Arabic
            - text_english (str): The text of the ayah in English
            - reference (str): The reference of the ayah
    """
    print(f"Fetching Quran ayah: {surah_num}:{ayah_num} with translation: {translation}")
    # Step 1: Get meta data to build surah → global ayah map
    meta_url = "http://api.alquran.cloud/v1/meta"
    meta_res = requests.get(meta_url)
    if meta_res.status_code != 200:
        raise Exception("Failed to fetch Quran metadata.")
    meta_data = meta_res.json()
    
    # Step 2: Build surah starting ayah map
    surah_refs = meta_data['data']['surahs']['references']
    surah_map = {}
    current_ayah = 1
    for surah in surah_refs:
        surah_map[surah['number']] = {
            'start_ayah': current_ayah,
            'englishName': surah['englishName'],
            'englishNameTranslation': surah['englishNameTranslation']
        }
        current_ayah += surah['numberOfAyahs']
    
    if surah_num not in surah_map:
        raise ValueError("Invalid surah number.")
    
    global_ayah = surah_map[surah_num]['start_ayah'] + ayah_num - 1
    
    # Step 3: Fetch the ayah using global number
    ayah_url = f"http://api.alquran.cloud/v1/ayah/{global_ayah}/{translation}"
    ayah_res = requests.get(ayah_url)
    if ayah_res.status_code != 200:
        raise Exception("Failed to fetch Quran ayah.")
    ayah_data = ayah_res.json()['data']
    
    # Step 4: Return structured info
    return {
        'surah': surah_map[surah_num]['englishName'],
        'translation': surah_map[surah_num]['englishNameTranslation'],
        'surah_number': surah_num,
        'ayah_number': ayah_num,
        'global_ayah': global_ayah,
        'text_arabic': ayah_data['text'],
        'text_english': ayah_data['edition']['name'] + ": " + ayah_data['text'],
        'reference': f"{surah_map[surah_num]['englishName']} ({surah_num}:{ayah_num})"
    }

@function_tool
async def search_islamic_content(query: str) -> dict:
    """Search the internet using Tavily and return structured results.

    This tool is designed to search the internet using Tavily and return structured results.

    Parameters
    ----------
    query : str
        The natural-language search query.

    Returns
    -------
    dict
        A dictionary matching Tavily's response schema, for example:

            {
              "query": "Who is Leo Messi?",
              "answer": "Lionel Messi ...",
              "images": [],
              "results": [
                  {"title": "...", "url": "...", "content": "...", "score": 0.81}
              ],
              "auto_parameters": {"topic": "general", "search_depth": "basic"},
              "response_time": "1.67"
            }

    Raises
    ------
    RuntimeError
        If environment variables cannot be loaded.
    """

    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=query,
        max_results=MAX_SEARCH_RESULTS,
        search_depth=SEARCH_DEPTH,
        include_images=False,
        include_videos=False,
        include_audio=False,
        include_files=False,
    )
    return response

@function_tool
async def verify_url_content(urls: list[str]) -> dict:
    """
    Extract text content from given URLs using Tavily's extraction API.
    
    Args:
        urls (list): The URLs to extract content from
        
    Returns:
        dict: A dictionary containing:
            - results (list): List of dictionaries with:
                - url (str): The URL that was extracted
                - raw_content (str): The extracted text content
                - images (list): List of image URLs found
            - failed_results (list): List of URLs that failed extraction
            - response_time (float): Time taken for the extraction
    """
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.extract(urls, include_images=False, extract_depth="advanced", format="markdown")
    return response

# islamic_content_verification_agent = Agent(
#     name="Islamic Content Verification Agent",
#     model=ISLAMIC_CONTENT_VERIFICATION_MODEL,
#     model_settings=ModelSettings(
#         temperature=ISLAMIC_CONTENT_VERIFICATION_TEMPERATURE,
#     ),
#     instructions=ISLAMIC_CONTENT_VERIFICATION_AGENT_PROMPT,
#     tools=[search_islamic_content, verify_url_content],
# )


@function_tool
async def islamic_verification_Custom(content: str = "Verify the islamic content validity and verify Quranic verses, Hadiths, and URLs for Islamic references and Authenticity. Once you have the required information, summarize it with cleanly formatted links for verification. Ensure you answer the question accurately and use markdown formatting. Prefer the 'fetch_quran_ayah' tool to verify Quranic verses, and the 'search_islamic_content' and 'verify_url_content' tools to verify Hadiths and URLs.") -> str:
    """A tool that runs the agent with custom configs to verify Islamic content.
    
    Args:
        content (str): The content to be verified for Islamic authenticity, including Quranic verses, Hadiths, or URLs claiming Islamic authority.
    """

    islamic_content_verification_agent = Agent(
        name="Islamic Content Verification Agent",
        model=ISLAMIC_CONTENT_VERIFICATION_MODEL,
        model_settings=ModelSettings(
            temperature=ISLAMIC_CONTENT_VERIFICATION_TEMPERATURE,
        ),
        instructions=ISLAMIC_CONTENT_VERIFICATION_AGENT_PROMPT,
        tools=[fetch_quran_ayah, search_islamic_content, verify_url_content],
    )

    result = await Runner.run(
        islamic_content_verification_agent,
        input=content,
        max_turns=50,
    )

    return str(result.final_output)