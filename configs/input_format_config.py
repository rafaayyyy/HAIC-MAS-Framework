# Dynamic Input Format Configuration for Z-Inspection Pipeline
# This allows the pipeline to analyze any type of content by simply changing the XML tag definitions


BLOG_INPUT_FORMAT_DESCRIPTION = """
You will receive content structured with XML tags:
- **<scenario>**: Contains the information about the ecosystem in which the scenario is taking place and user is interacting with the 
system.
- **<title>**: Contains the name/title of the blog being analyzed  
- **<content-to-be-analyzed>**: Contains the answer written by the LLM on the title question asked by the user.
"""

INPUT_FORMAT_DESCRIPTION = BLOG_INPUT_FORMAT_DESCRIPTION