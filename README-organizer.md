📂 Automated File Organizer

A Python-based background service for MX Linux (XFCE) that monitors the Downloads folder and automatically sorts files into categories based on their extensions.

🚀 Features

Real-time Monitoring: Uses the watchdog library to detect new files instantly.

Auto-Sorting: Categorizes files into Documents, Images, Audio, Videos, Archives, and Code.

Desktop Notifications: Sends a notify-send bubble in XFCE whenever a file is moved.

Lightweight: Runs in the background with minimal CPU usage.

🛠 Setup & Installation

1. Install Dependencies

This script requires the watchdog library. Install it for your user:

`pip install --user watchdog`


2. File Placement

Move the script to your scripts directory:

`mkdir -p ~/Scripts`
`mv organizer.py ~/Scripts/`


3. Autostart (MX Linux / XFCE)

To ensure the script runs every time you log in:

Open Settings Manager > Session and Startup.

Go to the Application Autostart tab.

Click + Add and enter:

Name: File Organizer

Command: `sh -c "sleep 5 && /usr/bin/python3 /home/$USER/Scripts/organizer.py"`

Trigger: on login

⌨️ Useful Zsh Aliases

Add these to your ~/.zshrc to manage the script easily from the terminal:

# Check if running
alias org-check='pgrep -fl organizer.py'

# Stop the script
alias org-stop='pkill -f organizer.py'

# Edit the script
alias org-edit='nano ~/Scripts/organizer.py'


⚙️ Configuration

You can customize the sorting logic by editing the DEST_DIRS dictionary in organizer.py:

DEST_DIRS = {
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Code": [".py", ".js", ".html", ".css", ".sh"]
}


📜 License

MIT License - Feel free to use and modify!
