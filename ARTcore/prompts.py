"""
Prompt templates and help documentation for ART system
"""

# Main help text
MAIN_HELP = """
ART HELP SYSTEM
==============

COMMANDS:
- ART: [query]      Run one query in offline mode regardless of current connection status
- help              Display this help message
- api:nanogpt       Switch to NanoGPT API mode
- api:grok          Switch to Grok API mode
- api:offline       Switch to offline mode
- status            Show current system status
- learn [filename]  Learn from a file in the learn folder
- generate report   Create a comprehensive PDF report with analytics
- weather           Get current weather information

MODE INFORMATION:
1. NanoGPT Mode - Uses the NanoGPT API for responses (requires API key)
2. Grok Mode    - Uses the Grok API for responses (requires API key)
3. Offline Mode - Uses only local data stored in ART_DB for responses

You can toggle between modes using the api: commands or using the interface switches.
"""

# Mode descriptions
MODE_DESCRIPTIONS = {
    "nanogpt": """
    🟢 NANOGPT MODE ACTIVE
    
    ART is now using NanoGPT API for responses.
    All queries will be processed through NanoGPT's language model.
    
    To switch to another mode, use 'api:grok' or 'api:offline'
    """,
    
    "grok": """
    🟢 GROK MODE ACTIVE
    
    ART is now using Grok API for responses.
    All queries will be processed through Grok's language model.
    
    To switch to another mode, use 'api:nanogpt' or 'api:offline'
    """,
    
    "offline": """
    🟢 OFFLINE MODE ACTIVE
    
    ART is now in offline mode.
    All queries will be processed using local data only.
    No external API calls will be made.
    
    To switch to another mode, use 'api:nanogpt' or 'api:grok'
    """
}

# Command specific help
COMMAND_HELP = {
    "art": """
    The ART: command temporarily forces offline mode for a single query.
    
    Usage: ART: [your question]
    
    Example: ART: What is the capital of France?
    
    This will process your question using only local data, regardless of 
    which connection mode is currently active. After this query, ART will
    return to the previously active connection mode.
    """,
    
    "api": """
    The api: commands switch between different connection modes.
    
    Available modes:
    - api:nanogpt - Use NanoGPT API
    - api:grok - Use Grok API
    - api:offline - Use offline mode
    
    Example: api:grok
    """,
    
    "learn": """
    The learn command processes and stores information from files.
    
    Usage: learn [filename]
    
    Example: learn wikipedia_article.txt
    
    Files must be placed in the ART_DB/ARTschool/learn folder first.
    Supported file types: .txt, .pdf, .py
    
    ART will read the file, create a summary, and store both the original
    content and the summary in its database for future reference.
    """,
    
    "report": """
    The generate report command creates a comprehensive system analysis in PDF format.
    
    Usage: generate report
    
    This will create a detailed PDF document containing:
    - System overview (uptime, database size, API status)
    - Data visualizations (charts showing dataset growth and uptime)
    - Knowledge acquisition summary (what ART has learned)
    - Performance metrics and statistics
    
    Reports are saved in the ARTreports folder with a timestamp in the filename.
    """
}

# Error messages
ERROR_MESSAGES = {
    "api_unavailable": "⚠️ {api_name} API is not available. Please check your API key in the .env file.",
    "offline_unavailable": "⚠️ Offline mode is not fully implemented yet. Some features may be limited.",
    "invalid_command": "⚠️ Invalid command. Type 'help' to see available commands.",
    "report_error": "⚠️ Error generating report: {error_message}. Make sure all required libraries are installed."
}

# Response templates
RESPONSE_TEMPLATES = {
    "thinking": "ART is thinking...",
    "offline_processing": "ART is processing your query offline...",
    "api_processing": "ART is querying {api_name}...",
    "system_update": "System updated: {message}",
    "report_generating": "Generating comprehensive system report. This might take a moment...",
    "report_success": "Report generated successfully at: {report_path}"
}