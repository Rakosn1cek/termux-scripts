#!/data/data/com.termux/files/usr/bin/bash
# 
# cheats.sh
# 
# Description: Launches a searchable fzf menu to instantly find and view 
# command syntax, tips, and reference material from local Markdown files 
# in the ~/.cheats directory.
#

# --- Configuration ---
CHEATS_DIR=~/.cheats
FZF_PROMPT="Cheat Sheet Search:"
# ---------------------

# Function to check and install fzf
check_installation() {
    if ! command -v fzf &> /dev/null; then
        echo "Fzf is not installed, but is required for the cheat sheet manager."
        read -r -p "Do you want to install it now? (y/n): " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            pkg install fzf -y
            if ! command -v fzf &> /dev/null; then
                echo "Error: fzf installation failed. Aborting." >&2
                return 1
            fi
            echo "Fzf installed successfully!"
        else
            echo "Fzf is required to run this utility. Aborting." >&2
            return 1
        fi
    fi
    return 0
}

# Function to parse and display the cheatsheet content
run_cheats_manager() {
    if [ ! -d "$CHEATS_DIR" ]; then
        echo "Error: Cheat sheets directory not found at $CHEATS_DIR." >&2
        echo "Please run the setup command: mkdir -p $CHEATS_DIR" >&2
        return 1
    fi
    
    # 1. Prepare the search content:
    #    Grep for Markdown headings (#, ##, ###) in all .md files in the cheats directory.
    
    local SEARCH_CONTENTS
    # Check if any .md files exist before running grep
    if ! ls "$CHEATS_DIR"/*.md &> /dev/null; then
        echo "Error: No cheat sheet files found in $CHEATS_DIR." >&2
        echo "To add a new cheatsheet, run: nano $CHEATS_DIR/topic.md" >&2
        echo "Ensure file names end in .md and contain headings (lines starting with #)." >&2
        return 1
    fi

    SEARCH_CONTENTS=$(
        grep -hE '^(#|##|###) ' "$CHEATS_DIR"/*.md | 
        sed -r 's/^(#+)\s*(.*)/\2/'
    )

    if [ -z "$SEARCH_CONTENTS" ]; then
        echo "Error: Found files in $CHEATS_DIR, but no headings (#, ##, or ###) were found." >&2
        echo "Please ensure your files start with Markdown headings." >&2
        return 1
    fi

    local selected_topic
    
    # 2. Launch fzf to select the desired topic/command.
    local selected_topic
    local HEADER_TEXT=$'Select a topic to view full details.\nPress ESC to exit.'
    
    selected_topic=$(
        printf '%s\n' "$SEARCH_CONTENTS" | 
        fzf --prompt="$FZF_PROMPT" \
            --header="$HEADER_TEXT" \
            --ansi \
            --reverse \
            --print0
    )
    
    # 3. If a topic was selected, find the content and display it.
    if [ -n "$selected_topic" ]; then
        # Remove null terminator
        selected_topic="${selected_topic%$'\0'}"
        
        echo "--- Details for: $selected_topic ---"
        
        # Use awk to find the block: start printing after the selected heading, 
        # and stop printing when the next heading (#) is encountered.
        awk "/#.*$selected_topic/{p=1; next} p && /^(#|##|###)/{p=0} p" "$CHEATS_DIR"/*.md | 
        less
    fi
}

# --- Main Execution ---
if check_installation; then
    run_cheats_manager
fi
