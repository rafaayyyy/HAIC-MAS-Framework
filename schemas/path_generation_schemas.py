from pydantic import BaseModel
from typing import List

class PathOption(BaseModel):
    """
    Individual path option for addressing Z-Inspection findings.
    """
    id: int  # Unique identifier for the path
    name: str  # Clear, descriptive title
    description: str  # Brief explanation of what this path does
    addresses_flags: List[str]  # Specific assess phase findings (e.g., "Privacy violation", "Bias detected")
    key_implementation_actions: List[str]  # Main steps to implement this path
    implementation_timeline: str = "TBD"  # Default to TBD if not specified
    complexity_assessment: str  # "Low", "Medium", or "High"
    impact_level: str  # "Low", "Medium", or "High"
    prerequisites: List[str]  # What needs to be in place before implementing

class StrategicGuidance(BaseModel):
    """
    Strategic guidance for implementing the paths.
    """
    priority_recommendation: str  # Which path(s) should be prioritized and why
    combined_approach: str  # How paths could work together
    implementation_considerations: str  # Important factors to consider when choosing paths

class PathGenerationResult(BaseModel):
    """
    Complete set of paths generated for addressing Z-Inspection findings.
    """
    final_paths: List[PathOption]  # All available path options
    strategic_guidance: StrategicGuidance  # Strategic guidance for implementation

    class Config:
        json_schema_extra = {
            "example": {
                "final_paths": [
                    {
                        "id": 1,
                        "name": "Enhanced Data Privacy Controls",
                        "description": "Implement comprehensive user data privacy controls and transparency measures.",
                        "addresses_flags": [
                            "Privacy and data governance: Insufficient user consent",
                            "Transparency: Lack of data usage clarity"
                        ],
                        "key_implementation_actions": [
                            "Develop granular privacy settings dashboard",
                            "Implement explicit consent mechanisms",
                            "Create data export and deletion functionality"
                        ],
                        "implementation_timeline": "Short-term (2–4 months)",
                        "complexity_assessment": "Medium",
                        "impact_level": "High",
                        "prerequisites": [
                            "Legal review of privacy requirements",
                            "Development resources for privacy infrastructure"
                        ]
                    },
                    {
                        "id": 2,
                        "name": "Algorithmic Bias Mitigation",
                        "description": "Implement bias detection and mitigation in recommendation algorithms.",
                        "addresses_flags": [
                            "Diversity, non-discrimination, and fairness: Bias in recommendations",
                            "Transparency: Unclear decision-making process"
                        ],
                        "key_implementation_actions": [
                            "Deploy bias detection tools",
                            "Implement demographic parity checks",
                            "Create diverse content promotion mechanisms"
                        ],
                        "implementation_timeline": "Long-term (6–12 months)",
                        "complexity_assessment": "High",
                        "impact_level": "High",
                        "prerequisites": [
                            "ML engineering expertise in fairness techniques",
                            "Diverse dataset for bias testing"
                        ]
                    }
                ],
                "strategic_guidance": {
                    "priority_recommendation": "Prioritize Path 1 for immediate compliance, followed by Path 2 for fairness.",
                    "combined_approach": "Privacy controls build trust while bias mitigation ensures equity.",
                    "implementation_considerations": "Monitor user adoption and establish clear success metrics."
                }
            }
        }