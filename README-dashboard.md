# 🖥️ Termux Command Center Dashboard (`dashboard.py`)

A Python script that acts as the personalized "Message of the Day" (MotD) or **Heads-Up Display (HUD)** for your Termux environment. It runs automatically upon starting the shell to provide an immediate status overview.

## ✨ Core Features

* **System Status:** Displays current disk space usage.
* **Integrated Status:** Pulls data directly from the **Budget-Buddy** and **Rich Task Manager** databases to provide a live summary.
* **Contextual Greeting:** Greets the user based on the time of day (Morning, Afternoon, Evening).
* **Clean Startup:** Clears the screen and, optionally, runs `neofetch` for a professional, clean command center look.
* **Version Tracking:** Displays the current script version (v1.0.0).

## 🚀 Setup and Automation

This script is designed to run automatically every time the Zsh shell starts.

1.  **File Location:** Ensure `dashboard.py` is saved in the `~/termux-scripts` directory.
2.  **Configuration Hook:** To make the dashboard run automatically, you must add the execution command to your `~/.zshrc` file.
    * Open `nano ~/.zshrc`.
    * Add this line **at the very bottom** of the file:

    ```bash
    python3 ~/termux-scripts/dashboard.py
    ```

3.  **Hiding Default Text (Optional):** To ensure only your custom dashboard appears (and to hide the default "Welcome to Termux!" help text), you cleared the system MotD file:

    ```bash
    echo > $PREFIX/etc/motd
    ```

## 📊 Data Integration Paths

The dashboard relies on finding the following files for status reports:

| Tool | File Path | Status Displayed |
| :--- | :--- | :--- |
| **Budget Buddy** | `~/Budget-Buddy-TUI/expenses.db` | Today's total spending. |
| **Rich Task Manager** | `~/rich-task-manager-tui/tasks.json` | Total number of pending tasks. |

