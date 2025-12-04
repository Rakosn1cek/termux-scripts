#!/data/data/com.termux/files/usr/bin/bash
# 
# screensaver.sh
# 
# Description: A utility script to install and run the 'cmatrix' 
# screensaver effect in Termux, providing multiple style options.
#

# --- Configuration ---
FZF_PROMPT="Select Screensaver Style:"
# ---------------------

# Function to check and install cmatrix
check_installation() {
    if ! command -v cmatrix &> /dev/null; then
        echo "Cmatrix is not installed."
        read -r -p "Do you want to install it now? (y/n): " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            pkg install cmatrix -y
            if ! command -v cmatrix &> /dev/null; then
                echo "Error: Cmatrix installation failed. Please check your network connection or try again." >&2
                return 1
            fi
            echo "Cmatrix installed successfully!"
        else
            echo "Cmatrix is required to run this screensaver. Aborting." >&2
            return 1
        fi
    fi
    return 0
}

# Function to display the selection menu and run the screensaver
run_screensaver() {
    # Key: Display Name | Command Arguments
    local OPTIONS=(
        "Matrix Rain (Default) | -u 10 -C green"
        "Binary Rain (Black & White) | -b -u 10 -C white"
        "Random Colors | -r -u 10"
        "Fast & Intense | -u 20 -C green"
        "Quit Screensaver | EXIT"
    )

    local selection
    
    # --- CRITICAL FIX ---
    # Use ANSI C Quoting ($'...') to make Bash interpret the \n as a newline character.
    local HEADER_TEXT=$'Choose a style and press ENTER to start.\nPress CTRL+C to stop the screensaver.'
    
    # Use fzf to select the option
    selection=$(
        printf '%s\n' "${OPTIONS[@]}" | 
        fzf --prompt="$FZF_PROMPT" \
            --delimiter='|' \
            --with-nth=1 \
            --header="$HEADER_TEXT" \
            --ansi \
            --reverse
    )

    if [[ -z "$selection" ]]; then
        echo "Selection cancelled."
        return 0
    fi
    
    # Extract the command arguments (the second field after '|')
    local ARGS=$(echo "$selection" | awk -F '|' '{print $2}' | xargs)

    if [[ "$ARGS" == "EXIT" ]]; then
        echo "Exiting screensaver utility."
        return 0
    fi

    echo "--- Starting Screensaver (Press CTRL+C to stop) ---"
    
    # Execute cmatrix with the selected arguments
    cmatrix $ARGS
    # The 'reset' command is run on exit to fix any terminal colors/state
    reset
    
    echo "Screensaver stopped."
}

# --- Main Execution ---
if check_installation; then
    run_screensaver
fi
