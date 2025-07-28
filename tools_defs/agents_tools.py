from agents_impl.ethical_agent import ethical_agent
from agents_impl.islamic_ethical_agent import islamic_ethical_agent
from agents_impl.path_generation_agent import path_generation_agent
from agents_impl.internal_docs_agent import internal_docs_agent
from agents_impl.linguistic_expert_agent import linguistic_expert_agent
from agents_impl.legal_agent import legal_agent

# Convert sub-agents into callable tools so the Orchestrator can invoke them and receive outputs
ethical_tool = ethical_agent.as_tool(
    tool_name="ethical_review",
    tool_description="Call this Z-Inspection ethical expert to analyze moral implications through the Z-Inspection lens, focusing on ethical violations, stakeholder harm assessment, trustworthy AI principles (EU HLEG guidelines), and ethical flags that may emerge in content/scenarios. Use for Z-Inspection ethical assessment or clarifying ethical concerns."
)

islamic_ethical_tool = islamic_ethical_agent.as_tool(
    tool_name="islamic_ethical_review",
    tool_description="Call this Z-Inspection Islamic ethics expert to analyze content/scenarios through Islamic ethical principles, Sharia compliance considerations, Islamic perspectives on fairness, and potential conflicts with Islamic teachings. Includes verification of Islamic sources cited through islamic_content_verification tool. Use for Z-Inspection Islamic ethical assessment or resolving tensions between Islamic values and content."
)

path_generation_tool = path_generation_agent.as_tool(
    tool_name="path_generation",
    tool_description="Call this Z-Inspection path generation expert to generate actionable solutions and strategic paths for addressing identified issues after Z-Inspection HLEG mapping by orchestrator agent. This agent creates concrete recommendations and implementation strategies."
)

internal_docs_tool = internal_docs_agent.as_tool(
    tool_name="internal_docs",
    tool_description="Call this Z-Inspection documentation assistant to get information about: (1) The Z-Inspection methodology and process steps from setup_phase.md, (2) Details about the system being analyzed from system_being_analyzed.md. This agent helps other agents understand the Z-Inspection process, their role in the project, and provides context about the system under evaluation. It can restructure queries and search across multiple project documents."
)

linguistic_expert_tool = linguistic_expert_agent.as_tool(
    tool_name="linguistic_expert",
    tool_description="Call this Z-Inspection linguistic expert to analyze the linguistic quality, clarity, accessibility barriers, cultural appropriateness, and communication effectiveness of text content. Provides detailed analysis of how linguistic issues might impact user trust, comprehension, and overall system credibility from a language and communication perspective."
)

legal_tool = legal_agent.as_tool(
    tool_name="legal_expert",
    tool_description="Call this Z-Inspection automated legal expert to analyze legal compliance, regulatory requirements, liability considerations, data protection laws (GDPR), accountability frameworks, and legal flags in content/scenarios. This is an LLM-based agent that provides initial legal assessment. Use for Z-Inspection legal assessment or resolving legal compliance contradictions."
)

# Export all agent tools
__all__ = [
    'ethical_tool',
    'islamic_ethical_tool', 
    'path_generation_tool',
    'internal_docs_tool',
    'linguistic_expert_tool',
    'legal_tool'
] 