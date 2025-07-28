# Global configuration for the Z-Inspection system

# =============================================================================
# SYSTEM UNDER ANALYSIS
# =============================================================================
# Description of the system being analyzed - used across all agents when querying about the system
system_llm = "System Being Analyzed: Fanar Based Islamic Writing Copilot System"


# Number of Domain Experts Agents
DOMAIN_EXPERT_AGENTS = 4

# Number of LLM Domain Experts Agents
LLM_DOMAIN_EXPERT_AGENTS = 3

# Number of Human Domain Experts
HUMAN_DOMAIN_EXPERT_AGENTS = 1

# =============================================================================
# MODEL CONFIGURATIONS
# =============================================================================
# Model used for domain expert agents (ethical, islamic ethics, linguistic, and legal agents)
# These agents require consistent, focused analysis
DOMAIN_EXPERT_MODEL = "o3"

# Model used for pipeline agents (orchestrator, path generator and recommendation agents)
# These agents handle workflow coordination and creative problem-solving
PIPELINE_MODEL = "o3"

# =============================================================================
# TEMPERATURE CONFIGURATIONS
# =============================================================================
# Temperature for domain expert agents
# Lower temperature (0.1) ensures more focused, consistent expert analysis
DOMAIN_EXPERT_TEMPERATURE = 1

# Temperature for pipeline agents
# Higher temperature (0.7) enables more creative problem-solving and recommendations
PIPELINE_TEMPERATURE = 1

# =============================================================================
# ISLAMIC CONTENT VERIFICATION AGENT SETTINGS
# =============================================================================
# Model for Islamic content verification (Quran, Hadith verification)
ISLAMIC_CONTENT_VERIFICATION_MODEL = "gpt-4.1"

# Temperature for Islamic content verification
# Moderate temperature (0.5) balances accuracy with contextual understanding
ISLAMIC_CONTENT_VERIFICATION_TEMPERATURE = 0.5

# Maximum number of search results to return from Tavily API
MAX_SEARCH_RESULTS = 5

# Search depth for Tavily API ("basic" or "advanced")
# Advanced provides more comprehensive results
SEARCH_DEPTH = "advanced"

# =============================================================================
# INTERNAL DOCUMENTATION AGENT SETTINGS
# =============================================================================
# Model for internal documentation search and retrieval
INTERNAL_DOCS_AGENT_MODEL = "gpt-4.1"

# Temperature for internal docs agent
# Moderate temperature (0.5) for balanced information retrieval
INTERNAL_DOCS_AGENT_TEMPERATURE = 0.5


# =============================================================================

# Human Agents
HUMAN_EXPERTS_MODEL = "gpt-4.1"

# Temperature for human experts
# Moderate temperature (0.5) for balanced information retrieval
HUMAN_EXPERTS_TEMPERATURE = 0.5

