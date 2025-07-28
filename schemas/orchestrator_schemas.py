from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class ZInspectionQuery(BaseModel):
    """
    Structured query object sent TO sub-agents for analysis.
    """
    original_content: str  # Contains XML-tagged scenario with <title> and <content-to-be-analyzed>
    analysis_query: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "original_content": """
                <scenario>A user is interacting with a copilot about Healthcare Blog Post</scenario>
                <title>Healthcare Blog Post</title>
                <content-to-be-analyzed>
                This blog post discusses various healthcare topics including patient privacy, medical ethics, and healthcare accessibility. It covers topics such as:

                1. Patient data protection practices
                2. Ethical considerations in medical research  
                3. Healthcare equity and access issues
                4. Medical professional responsibilities
                5. Public health policy implications

                The content aims to inform readers about important healthcare considerations while maintaining professional standards.
                </content-to-be-analyzed>
                """,
                "analysis_query": "Analyze this healthcare blog content for Z-Inspection compliance and ethical considerations",
            }
        }

class AgentInteraction(BaseModel):
    """
    Single interaction with a sub-agent during Z-Inspection.
    """
    agent_name: str  # Which expert agent was called
    iteration: int  # Which iteration this was part of (1, 2, or 3)
    analysis_query: str  # Just the analysis query part (without the full XML content)
    response_received: str  # Complete response from the agent
    purpose: str  # Why this agent was called (initial analysis, clarification, verification)

class EthicalFlag(BaseModel):
    """
    Individual ethical flag identified during Z-Inspection.
    """
    flag_description: str
    source_expert: str  # Which Z-Inspection expert identified this
    evidence: str  # Specific quotes/reasoning from expert
    hleg_mapping: str  # Which HLEG requirement this violates and why
    severity: str  # Critical, High, Medium, Low

class ZInspectionWorkflow(BaseModel):
    """
    Complete Z-Inspection workflow capturing the essential process data.
    """
    scenario_title: str  # Extracted from <title> tags
    scenario_summary: str  # Brief summary of the content/scenario analyzed
    original_xml_content: str  # Complete original XML content received (stored once)
    total_iterations: int  # How many iterations were performed
    agent_interactions: List[AgentInteraction]  # All interactions with sub-agents (without repeated XML)
    ethical_flags: List[EthicalFlag]  # All identified ethical issues
    hleg_impacts_summary: str  # Overview of which HLEG requirements are affected
    hleg_violations_detail: Dict[str, List[str]]  # Detailed mapping of HLEG violations
    orchestrator_reasoning: str  # Orchestrator's final reasoning and synthesis
    agents_consulted: List[str]  # Which expert agents were used
    total_flags_identified: int  # Count of ethical flags
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario_title": "Healthcare Blog Post",
                "scenario_summary": "A blog post discussing healthcare topics including patient privacy, medical ethics, and healthcare accessibility.",
                "original_xml_content": "<scenario>A user is interacting with a copilot about Healthcare Blog Post</scenario><title>Healthcare Blog Post</title><content-to-be-analyzed>Blog content...</content-to-be-analyzed>",
                "total_iterations": 2,
                "agent_interactions": [
                    {
                        "agent_name": "Ethical Agent",
                        "iteration": 1,
                        "analysis_query": "Analyze this scenario from the perspective of general ethics and HLEG trustworthy principles. Identify any potential ethical flags in the content.",
                        "response_received": "The scenario presents several ethical concerns...",
                        "purpose": "initial analysis"
                    }
                ],
                "ethical_flags": [
                    {
                        "flag_description": "Patient data privacy concerns in healthcare discussions",
                        "source_expert": "Ethical Agent",
                        "evidence": "The content discusses patient data without explicit privacy safeguards mentioned",
                        "hleg_mapping": "Violates HLEG Requirement 3 (Privacy and Data Governance)",
                        "severity": "High"
                    }
                ],
                "hleg_impacts_summary": "Primary concerns in Privacy & Data Governance (Req 3) and Transparency (Req 4)",
                "hleg_violations_detail": {
                    "Privacy and Data Governance": ["Inadequate data protection measures", "Missing consent frameworks"],
                    "Transparency": ["Lack of clear privacy policies", "Insufficient user information"]
                },
                "orchestrator_reasoning": "Based on expert consultations, the scenario presents significant privacy concerns...",
                "agents_consulted": ["Ethical Agent", "Islamic Ethical Agent"],
                "total_flags_identified": 3
            }
        }

# Legacy class for backward compatibility
class ZInspectionResult(BaseModel):
    """
    Simplified result object (legacy - use ZInspectionWorkflow for complete data).
    """
    scenario_title: str
    scenario_summary: str
    ethical_flags: List[EthicalFlag]
    hleg_impacts_summary: str 