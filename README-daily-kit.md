# 🛠️ Termux Daily Kit (`daily_kit.sh`)

This is a scheduled **Bash script** designed to automate routine maintenance, updates, and backups within the Termux environment. It ensures system health and automatically secures local changes to the GitHub repository.

## ✨ Core Features (v1.0.0)

* **Package Updates:** Runs `pkg update && pkg upgrade -y` to keep all system packages current.
* **Cleanup:** Runs `termux-clean` to remove unnecessary files and packages.
* **Auto-Backup:** Automatically checks the `~/termux-scripts` repository for uncommitted changes, performs an automatic commit (`AUTOBACKUP`), and pushes those changes to GitHub.
* **Automatic Execution:** Designed to run silently and periodically using `cron`.

## 🚀 Setup and Scheduling

This script is meant to be run automatically, usually once per day.

### 1. Cron Setup

You must install and configure the **Cron daemon** in Termux for scheduling:

1.  **Install Cron:**
    ```bash
    pkg install termux-services termux-cron -y
    ```
2.  **Edit Crontab:** Open the crontab file to define the schedule.
    ```bash
    crontab -e
    ```
3.  **Add the Schedule:** Add the following line to run the script **every day at 3:00 AM** (You can adjust `0 3`):

    ```cron
    0 3 * * * /data/data/com.termux/files/home/termux-scripts/daily_kit.sh >> /dev/null 2>&1
    ```
    *Note: The full path to the script is required for Cron.*

### 2. Automated Git Backup Requirements

For the script to push changes automatically without prompting for credentials, you must cache your GitHub Personal Access Token (PAT):

* **Cache Credentials (for 1 hour):** This is useful for testing.
    ```bash
    git config --global credential.helper 'cache --timeout=3600'
    ```
* **Full Automation:** For long-term non-interactive use, consider using the `store` credential helper (less secure but persistent) or SSH keys, configured specifically for non-interactive Termux sessions.

## 💡 Usage Examples

The script is primarily run by the system (cron), but you can manually execute it for testing:

```bash
# Manual execution
/data/data/com.termux/files/home/termux-scripts/daily_kit.sh

# Check the script version
/data/data/com.termux/files/home/termux-scripts/daily_kit.sh --version

