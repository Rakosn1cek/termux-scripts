#!/bin/bash
VERSION="1.1.0"

# Function to show version (add this near the top)
show_version() {
    echo "Daily Kit Version: v$VERSION"
    exit 0
}

# --- 1. Shebang & Variables ---

# Define Color Codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Define Key Directories and Filenames
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/sdcard/TermuxBackups" # Assumes you ran termux-setup-storage
BACKUP_FILENAME="termux_daily_backup_$TIMESTAMP.tar.gz"

# List of critical files/folders to back up (relative to $HOME)
# NOTE: Ensure these paths exist!
BACKUP_TARGETS=(
    "Budget-Buddy-TUI/settings.db"
    "Budget-Buddy-TUI/expenses.db"
    "rich-task-manager-tui/tasks.json"
    ".zshrc"          # Your shell configurations
    ".bashrc"         # Keep this in case you use Bash for non-interactive scripts
    # Add any other important dotfiles or scripts here!
)

# Check for version flag
if [[ "$1" == "--version" ]]; then
    show_version
fi

# --- 2. Logging Function ---
log() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date +'%Y-%m-%d %H:%M:%S')] $message${NC}"
}

# --- 3. Check for Termux ---
if [[ -z "$TERMUX_VERSION" ]]; then
    log $RED "ERROR: This script is intended to run in Termux."
    exit 1
fi

log $GREEN "--- Daily Kit Initiated ---"
echo ""

# --- PHASE 2: MAINTENANCE AND CLEANUP ---

log $YELLOW "Starting Termux package update and upgrade..."
pkg update -y && pkg upgrade -y

if [ $? -eq 0 ]; then
    log $GREEN "Termux packages updated successfully."
else
    log $RED "Termux package update failed!"
fi
echo ""

log $YELLOW "Running system cleanup..."
termux-cleanup 
log $YELLOW "Clearing APT package cache..."
pkg clean
log $GREEN "System cleanup complete."
echo ""

log $YELLOW "Checking Termux home directory size..."
DU_OUTPUT=$(du -sh $HOME)
log $GREEN "Home Directory Size: $DU_OUTPUT"
echo ""

# --- PHASE 3: BACKUP STRATEGY ---

log $YELLOW "Starting critical data backup..."

# 1. Create the backup directory if it doesn't exist
if [ ! -d "$BACKUP_DIR" ]; then
    log $YELLOW "Creating backup directory: $BACKUP_DIR"
    mkdir -p "$BACKUP_DIR"
fi

# 2. Use 'tar' to archive and compress the targets
# -c: create archive, -z: compress with gzip, -f: output to file
# -P: don't strip leading slashes (important for absolute paths, though we use relative here)
# -C $HOME: change directory to $HOME before operation, allowing us to use relative paths cleanly
# ${BACKUP_TARGETS[@]}: expands the array into a list of arguments for tar
tar -czf "$BACKUP_DIR/$BACKUP_FILENAME" -C "$HOME" "${BACKUP_TARGETS[@]}"

if [ $? -eq 0 ]; then
    log $GREEN "Backup successful! Archive created: $BACKUP_FILENAME"
    log $GREEN "File location: $BACKUP_DIR"
    
    # Optional: Delete backups older than 7 days
    log $YELLOW "Removing backups older than 7 days..."
    find "$BACKUP_DIR" -type f -name 'termux_daily_backup_*.tar.gz' -mtime +7 -delete
    log $GREEN "Old backups cleaned up."
else
    log $RED "Backup failed! Check file paths and permissions."
fi

echo ""
log $GREEN "--- Daily Kit Finished! Have a productive day! ---"
# Start the cron daemon for scheduled jobs
pgrep -x crond || crond
