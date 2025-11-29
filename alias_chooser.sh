#!/bin/bash
# alias_chooser.sh - Reads the aliases.md file and presents a menu via fzf.
# The selected command is then printed for the parent shell to execute via 'eval'.

ALIAS_FILE="$HOME/aliases.md"
EXEC_DELIMITER="___EXECUTE_ALIAS___"
FZF_PROMPT="» Select Command: "

# 1. Check for fzf installation
if ! command -v fzf &> /dev/null
then
    echo -e "\033[0;31mError: fzf is required but not installed. Run: pkg install fzf\033[0m" >&2
    exit 1
fi

# 2. Process the aliases.md file and run fzf
# The output from fzf will be the entire selected line (e.g., "bb | Launch the Budget Buddy app").

chosen_line=$(
    grep -v '^#' "$ALIAS_FILE" |        # Filter out comment lines
    grep -v '^\s*$' |                   # Filter out blank lines
    awk -F '|' '{print $1 " | " $2}' |  # Format output for fzf

    fzf --prompt="$FZF_PROMPT" \
        --ansi \
        --header="Fuzzy search for commands (Format: Command | Description)" \
        --reverse 
)

# 3. Execution Logic
if [[ -n "$chosen_line" ]]; then
    
    # Extract only the command part (everything before the first pipe)
    # The tr -d '[:space:]' removes any leading/trailing whitespace around the command.
    COMMAND_TO_RUN=$(echo "$chosen_line" | awk -F '|' '{print $1}' | tr -d '[:space:]')
    
    # Send the final command back to the parent shell with the delimiter.
    echo "${EXEC_DELIMITER}${COMMAND_TO_RUN}"
fi
