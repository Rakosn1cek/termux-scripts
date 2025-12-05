#!/data/data/com.termux/files/usr/bin/bash
# 
# ddm.sh
# 
# Description: Automates daily maintenance tasks, including system updates, 
# cleanup, and Git status checks for the main scripts repository.
#

# --- Configuration ---
SCRIPTS_DIR="$HOME/termux-scripts"
COLOR_YELLOW="\033[93m"
COLOR_GREEN="\033[92m"
COLOR_CYAN="\033[96m"
COLOR_RED="\033[91m"
COLOR_RESET="\033[0m"
# ---------------------

echo -e "${COLOR_CYAN}===========================================${COLOR_RESET}"
echo -e "${COLOR_CYAN}  DAILY DRIVER MAINTENANCE DASHBOARD (DDM) ${COLOR_RESET}"
echo -e "${COLOR_CYAN}===========================================${COLOR_RESET}"

# --- 1. System Maintenance and Cleanup ---
echo -e "\n${COLOR_YELLOW}--- 1. System Updates & Cleanup ---${COLOR_RESET}"
echo "Running pkg update and upgrade..."

# Update and Upgrade (using non-interactive mode -y)
if pkg update && pkg upgrade -y; then
    echo -e "${COLOR_GREEN}✔ System packages updated successfully.${COLOR_RESET}"
else
    echo -e "${COLOR_RED}✘ Package update or upgrade failed.${COLOR_RESET}"
fi

# Clean the package cache
echo "Cleaning package cache..."
if pkg clean; then
    echo -e "${COLOR_GREEN}✔ Cache cleaned.${COLOR_RESET}"
else
    echo -e "${COLOR_RED}✘ Cache cleanup failed.${COLOR_RESET}"
fi


# --- 2. Git Status Check ---
echo -e "\n${COLOR_YELLOW}--- 2. Git Repository Status ---${COLOR_RESET}"

if [ -d "$SCRIPTS_DIR" ] && [ -d "$SCRIPTS_DIR/.git" ]; then
    echo "Checking status for: ${SCRIPTS_DIR}"
    
    cd "$SCRIPTS_DIR" || { echo -e "${COLOR_RED}Could not change directory to $SCRIPTS_DIR.${COLOR_RESET}"; exit 1; }

    # Fetch latest changes from remote to check divergence without merging
    git fetch origin --quiet

    # Check for unstaged and staged changes
    if git status --porcelain | grep -q .; then
        echo -e "${COLOR_RED}⚠ UNCOMMITTED CHANGES DETECTED:${COLOR_RESET}"
        git status --short
    else
        echo -e "${COLOR_GREEN}✔ No local changes detected.${COLOR_RESET}"
    fi

    # Check if local is ahead or behind remote
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    BASE=$(git merge-base @ @{u})

    if [ "$LOCAL" = "$REMOTE" ]; then
        echo -e "${COLOR_GREEN}✔ Repository is up-to-date with origin.${COLOR_RESET}"
    elif [ "$LOCAL" = "$BASE" ]; then
        echo -e "${COLOR_YELLOW}↓ Repository is BEHIND remote. Needs 'git pull'.${COLOR_RESET}"
    elif [ "$REMOTE" = "$BASE" ]; then
        echo -e "${COLOR_YELLOW}↑ Repository is AHEAD of remote. Needs 'git push'.${COLOR_RESET}"
    else
        echo -e "${COLOR_RED}↔ Repository has diverged. Manual intervention needed.${COLOR_RESET}"
    fi

    # Return to the previous directory
    cd - > /dev/null
else
    echo -e "${COLOR_RED}✘ Git repository not found at $SCRIPTS_DIR.${COLOR_RESET}"
fi

echo -e "\n${COLOR_CYAN}===========================================${COLOR_RESET}"
echo -e "${COLOR_GREEN}DAILY MAINTENANCE COMPLETE!${COLOR_RESET}"
echo -e "${COLOR_CYAN}===========================================${COLOR_RESET}"
