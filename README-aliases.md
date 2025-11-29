Alias Command Chooser (v1.0.0)
The Alias Command Chooser provides an interactive, searchable menu for executing frequently used, longer commands or aliases defined in the user's shell environment.
This system replaces the need to remember many different shell aliases by consolidating them into a single command (cmd) managed by the powerful Fuzzy Finder (fzf).
🚀 How to Use
Simply type the function name in your terminal:
cmd

This opens a full-screen, searchable menu powered by fzf. Type any part of the command or description to filter the list instantly. Press Enter on the selection to execute the corresponding command immediately in your shell.
🛠️ Setup and Structure
This utility relies on three components:
| File / Component | Purpose | Location |
|---|---|---|
| aliases.md | Data Source: A plain text file containing the list of commands and descriptions. This is the only file you need to manually edit. | ~/aliases.md |
| alias_chooser.sh | Logic Script: The Bash script that reads aliases.md, formats the output, and runs fzf. It passes the chosen command back to the shell via a special marker. | ~/alias_chooser.sh |
| cmd function | Shell Hook: The function defined in ~/.zshrc that executes the script and uses eval to run the output command in the current shell session. | ~/.zshrc |
📚 Maintaining the Command List (~/aliases.md)
The file uses a simple, pipe-delimited format:
<Command> | <Description>

Example entries:
# Command | Description

note add | Quickly create a new timestamped note entry
rtm | Launch the Rich Task Manager (shell alias)
python3 ~/termux-scripts/dashboard.py | Run the main system dashboard script

NOTE: The system automatically removes all leading/trailing whitespace around the command when executing it, so spacing in your aliases.md file does not matter.
⚙️ Configuration (For Debugging)
If you need to debug, the system relies on the following logic in ~/.zshrc:
# The 'cmd' function captures the output of the script, 
# filters for the '___EXECUTE_ALIAS___' delimiter, removes it, and runs the result.



