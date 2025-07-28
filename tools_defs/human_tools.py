from human_agents_impl.legal_human import legal_human_agent
from human_agents_impl.ui_ux_human import ui_ux_human_agent
from human_agents_impl.technical_human import technical_human_agent

# Convert human expert agents into callable tools so the Orchestrator can invoke them and receive outputs
legal_human_tool = legal_human_agent.as_tool(
    tool_name="legal_review",
    tool_description="This is a human expert agent that requires human CLI/File input. Call this Z-Inspection human legal expert to get professional legal analysis of compliance, regulatory requirements, liability considerations, data protection laws, accountability frameworks, and legal flags in content/scenarios. Provides expert-level legal assessment from a qualified human legal professional. Use for Z-Inspection legal assessment or resolving complex legal compliance contradictions."
)

ui_ux_human_tool = ui_ux_human_agent.as_tool(
    tool_name="ui_ux_review",
    tool_description="This is a human expert agent that requires human CLI/File input. Call this Z-Inspection human UI/UX expert to get professional analysis of user interface design, user experience patterns, accessibility compliance, usability standards, and design ethics in content/scenarios. Provides expert-level UI/UX assessment from a qualified human design professional. Use for Z-Inspection UI/UX assessment or resolving design and usability issues."
)

technical_human_tool = technical_human_agent.as_tool(
    tool_name="technical_review",
    tool_description="This is a human expert agent that requires CLI input. Call this Z-Inspection human technical expert to get professional analysis of code ethics, software architecture, security considerations, system robustness, maintainability, and technical trustworthiness factors in content/scenarios, especially for codebase analysis. Provides expert-level technical assessment from a qualified human software professional. Use for Z-Inspection technical assessment or clarifying complex technical aspects that impact trustworthiness."
)

# Export all human expert tools
__all__ = [
    'legal_human_tool',
    'ui_ux_human_tool',
    'technical_human_tool'
] 