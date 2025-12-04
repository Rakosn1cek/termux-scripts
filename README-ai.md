Gemini CLI Assistant (ai.py or gi)
A command-line interface (CLI) assistant built for Termux environments, powered by the Gemini API. This tool allows for instant lookups of Linux commands, syntax, and quick facts using natural language, directly from your terminal.
The script uses Google Search grounding to provide up-to-date and factual information.
🚀 Setup & Dependencies
 * Install Python and Requests:
   pkg install python
pip install requests

 * Save the Script: Place ai.py in your executable scripts directory (e.g., ~/termux-scripts/).
   chmod +x ~/termux-scripts/ai.py

🔑 Authentication (API Key)
This script requires a Gemini API key. DO NOT commit your API key to GitHub.
 * Get a Key: Obtain a free API key from Google AI Studio.
 * Set Environment Variable: Add the following line to the end of your shell configuration file (~/.zshrc or ~/.bashrc), replacing the placeholder with your actual key:
   export GEMINI_API_KEY='YOUR_KEY_HERE'

 * Reload Shell:
   source ~/.zshrc

💡 Usage
Create aliases for quick access to the script using a short command like ai or gi.
# Add these lines to your shell config:
alias ai='python ~/termux-scripts/ai.py'
alias gi='python ~/termux-scripts/ai.py'

Examples
Ask a command question:
gi "how do I rename a file in termux"

# Expected Output:
# >>> Gemini Response:
# The `mv` command (move) is used to rename a file.
# mv current_file_name new_file_name

Ask a general question:
ai "what are the most important packages to install on termux"


