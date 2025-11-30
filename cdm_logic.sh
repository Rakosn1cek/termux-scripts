#!/bin/bash
# cdm_logic.sh - Handles saving bookmarks and generating fzf output.

BOOKMARKS_FILE="$HOME/cd_bookmarks.txt"
FZF_PROMPT="» Jump to: "

# Function to save the current directory
save_bookmark() {
    local NICKNAME="$1"
    local CURRENT_DIR="$2"

    if [[ -z "$NICKNAME" ]]; then
        echo "Error: Must provide a nickname to save. Usage: cdm save <nickname>" >&2
        return 1
    fi
    
    # Check if the nickname already exists (case-insensitive)
    if grep -iq "^$NICKNAME:" "$BOOKMARKS_FILE" 2>/dev/null; then
        echo "Error: Nickname '$NICKNAME' already exists. Use 'cdm delete' first if you need to replace it." >&2
        return 1
    fi

    # Append the new bookmark: NICKNAME:PATH
    echo "$NICKNAME:$CURRENT_DIR" >> "$BOOKMARKS_FILE"
    echo "✅ Saved bookmark '$NICKNAME' -> $CURRENT_DIR"
}

# Function to display the fzf menu and output the selected path
jump_menu() {
    # Check if the file exists and is not empty
    if [[ ! -f "$BOOKMARKS_FILE" ]] || [[ ! -s "$BOOKMARKS_FILE" ]]; then
        echo "Error: No bookmarks found. Use 'cdm save <nickname>' first." >&2
        return 1
    fi

    local selected_line
    
    selected_line=$(
        # 1. Awk reads the file using ':' as the field separator, 
        #    then prints the Nickname ($1) and the Path ($2), separated by our custom '###' delimiter.
        awk -F ':' '{printf "%-20s###%s\n", $1, $2}' "$BOOKMARKS_FILE" |
        
        # 2. Run fzf on the formatted lines. We let fzf return the WHOLE line.
        fzf --prompt="$FZF_PROMPT" \
            --ansi \
            --header="Fuzzy search nicknames and paths." \
            --reverse 
            # Note: We REMOVE --with-nth and --delimiter flags from fzf
    )

    if [[ -n "$selected_line" ]]; then
        local COMMAND_TO_RUN
        
        # 3. CRITICAL STEP: Use awk to split the selected line by '###' and take only the second field (the path).
        COMMAND_TO_RUN=$(echo "$selected_line" | awk -F '###' '{print $2}')
        
        # The output of the script must be the final directory path.
        echo "$COMMAND_TO_RUN"
    fi
}

# Main routing for the script
case "$1" in
    save)
        # $2 is the nickname, $3 is the current path passed from the Zsh function
        save_bookmark "$2" "$3"
        ;;
    jump)
        jump_menu
        ;;
    *)
        echo "Usage: cdm save <nickname> | cdm jump" >&2
        return 1
        ;;
esac
