# 🏗️ New Project Generator (`new-project.sh`) v1.1.0

A powerful Bash script designed to automate the tedious parts of starting a new coding project. It ensures every new project begins with proper folder structure, Git version control, and boilerplate files.

## ✨ Core Features (v1.1.0)

* **Project Root:** All projects are created within the dedicated `$HOME/Projects` directory.
* **Git Initialization:** Automatically initializes a Git repository (`git init`) and performs an initial commit.
* **Boilerplate:** Creates a base `README.md` file for immediate documentation.
* **Type Support:** Handles specialized setup for different project types:
    * **Python/Py:** Creates a `.venv` virtual environment directory and a starter `main.py` file, and adds `.venv` to `.gitignore`.
    * **Bash/Sh:** Creates a starter executable script (`run.sh`) with the correct shebang (`#!/bin/bash`).
    * **Generic:** Creates a default `notes.txt` file.
* **Version Tracking:** Displays the current script version.

## 🚀 Usage

The script is executed manually and is fully interactive, prompting you for the required details.

```bash
# Execute the generator
~/termux-scripts/new-project.sh

Supported Project Types
​When prompted for the project type, enter one of the following:
| Tool | Script | Primary Function | Status |
| :--- | :--- | :--- | :--- |
| **Project Generator** | `new-project.sh` | Automates project setup, Git initialization, and venv creation. | **Complete** |
| **Knowledge Base** | `kb.py` | CLI note-taking with advanced search, view, and tag filtering. | **Complete** |
| **Daily Kit** | `daily_kit.sh` | Scheduled maintenance, updates, and automatic Git backups. | **Complete** |
| **Dashboard** | `dashboard.py` | Automatic startup HUD displaying system stats, tasks, and budget. | **Complete** |

💡 Example Session

~/termux-scripts/new-project.sh
# Enter new project name (e.g., termux-logger): my-telegram-bot
# Enter project type (e.g., py): py
#
# ✅ Created project directory: .../Projects/my-telegram-bot
# ✅ Initialized Git repository.
# Setting up Python Virtual Environment...
# ✅ Initial commit complete. Project is ready!
# Starter File: main.py
# Next Step: cd my-telegram-bot && source .venv/bin/activate

