#!/bin/bash
# new-project.sh - Automated Project Generator (v1.1.0)

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
RESET='\033[0m'

# Define Project Root Directory
PROJECT_ROOT="$HOME/Projects"
VERSION="1.1.0"

# --- Functions ---

# Function to display the header
header() {
    echo -e "${BOLD}${CYAN}---------------------------------------------${RESET}"
    echo -e "${BOLD}${CYAN}   New Project Generator (v$VERSION)         ${RESET}"
    echo -e "${BOLD}${CYAN}---------------------------------------------${RESET}"
}

# Function for clean project setup
setup_project() {
    local PROJECT_NAME="$1"
    local PROJECT_TYPE="$2"
    local STARTER_FILE=""

    # 1. Create directory
    if [ ! -d "$PROJECT_ROOT" ]; then
        mkdir -p "$PROJECT_ROOT"
    fi
    cd "$PROJECT_ROOT" || { echo -e "${RED}Error: Could not navigate to project root.${RESET}"; exit 1; }

    if [ -d "$PROJECT_NAME" ]; then
        echo -e "${RED}Error: Directory '$PROJECT_NAME' already exists. Aborting.${RESET}"
        exit 1
    fi
    mkdir "$PROJECT_NAME"
    cd "$PROJECT_NAME"

    echo -e "${GREEN}✅ Created project directory: $PROJECT_ROOT/$PROJECT_NAME${RESET}"
    
    # 2. Initialize Git
    git init > /dev/null 2>&1
    echo -e "${GREEN}✅ Initialized Git repository.${RESET}"
    
    # 3. Create README.md boilerplate
    echo "# $PROJECT_NAME" > README.md
    echo -e "\n## Description\n\nThis is a new $PROJECT_TYPE project." >> README.md
    
    # 4. Handle type-specific setup
    case "$PROJECT_TYPE" in
        python|py)
            echo -e "${CYAN}Setting up Python Virtual Environment...${RESET}"
            # Check for Python virtual environment tool
            if ! command -v python -m venv &> /dev/null; then
                echo -e "${RED}Warning: 'python -m venv' not found. Installing now...${RESET}"
                pkg install python -y
            fi
            
            # Create venv
            python -m venv .venv 
            
            # Create starter file
            STARTER_FILE="main.py"
            echo "#!/usr/bin/env python3" > "$STARTER_FILE"
            echo -e "\nprint('Hello, $PROJECT_NAME!')" >> "$STARTER_FILE"
            
            # Add venv to gitignore
            echo ".venv/" > .gitignore
            echo "__pycache__/" >> .gitignore
            ;;

        bash|sh)
            echo -e "${CYAN}Setting up Bash script...${RESET}"
            STARTER_FILE="run.sh"
            echo "#!/bin/bash" > "$STARTER_FILE"
            echo -e "\n# Version 1.0.0" >> "$STARTER_FILE"
            echo -e "\necho 'Hello, Termux! This is $PROJECT_NAME.'" >> "$STARTER_FILE"
            chmod +x "$STARTER_FILE"
            ;;
        
        *)
            # Default for generic/other projects
            echo -e "${CYAN}Setting up generic project structure.${RESET}"
            STARTER_FILE="notes.txt"
            echo "Project $PROJECT_NAME started on $(date +'%Y-%m-%d')" > "$STARTER_FILE"
            ;;
    esac

    # 5. Git initial commit
    git add .
    git commit -m "feat: Initial setup for $PROJECT_NAME ($PROJECT_TYPE) project." > /dev/null
    echo -e "${GREEN}✅ Initial commit complete. Project is ready!${RESET}"
    
    # 6. Final Steps
    if [ -n "$STARTER_FILE" ]; then
        echo -e "${BOLD}${YELLOW}Starter File: $STARTER_FILE${RESET}"
    fi
    echo -e "\n${BOLD}${CYAN}Project Directory:${RESET} $PWD"
    echo -e "${BOLD}${CYAN}Next Step:${RESET} cd $PROJECT_NAME && source .venv/bin/activate"
    echo -e "\n${BOLD}${CYAN}---------------------------------------------${RESET}"
}

# --- Main Logic ---

header

# Prompt 1: Project Name (using echo for prompt)
echo -en $'\n'"Enter new project name (e.g., termux-logger): "
read -r NAME
if [ -z "$NAME" ]; then
    echo -e "${RED}Error: Project name cannot be empty.${RESET}"
    exit 1
fi

# ... (rest of Prompt 1 code) ...

# Prompt 2: Project Type (using echo for prompt)
echo -e "${BOLD}${YELLOW}\nAvailable Types: python/py, bash/sh, or [generic]${RESET}"
echo -en "Enter project type (e.g., py): "
read -r TYPE

# ... (rest of Main Logic) ...


# Set type to lowercase for case statement
TYPE=$(echo "$TYPE" | tr '[:upper:]' '[:lower:]')

# Call the setup function
setup_project "$NAME" "$TYPE"

