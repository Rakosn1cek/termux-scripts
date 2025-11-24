#!/usr/bin/env python3
import os
import sqlite3
import json
import shutil
import subprocess
from datetime import datetime
VERSION= "1.1.1"

# --- Configuration & Paths ---
# Using the paths you provided earlier
BUDGET_DB = os.path.expanduser("~/Budget-Buddy-TUI/expenses.db")
TASKS_JSON = os.path.expanduser("~/rich-task-manager-tui/tasks.json")

# Colors
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

def get_greeting():
    hour = datetime.now().hour
    if hour < 12: return "Good Morning"
    elif hour < 18: return "Good Afternoon"
    else: return "Good Evening"

def get_system_stats():
    # Get disk usage for the home directory
    total, used, free = shutil.disk_usage(os.path.expanduser("~"))
    free_gb = free // (2**30)
    return f"{free_gb} GB Free"

def get_pending_tasks():
    if not os.path.exists(TASKS_JSON):
        return f"{RED}Task file not found{RESET}"
    
    try:
        with open(TASKS_JSON, 'r') as f:
            tasks = json.load(f)
            # Assuming tasks have a 'status' or 'completed' field. 
            # Adjusting logic to count items that are NOT done.
            pending = 0
            for task in tasks:
                # Check for common status keys (adjust based on your actual JSON structure)
                is_done = task.get('completed', False) or task.get('status') == 'done'
                if not is_done:
                    pending += 1
            return f"{YELLOW}{pending} Tasks Pending{RESET}"
    except Exception:
        return f"{RED}Error reading tasks{RESET}"

def get_todays_spending():
    if not os.path.exists(BUDGET_DB):
        return f"{RED}Budget DB not found{RESET}"
    
    try:
        conn = sqlite3.connect(BUDGET_DB)
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        
        # QUERY: Sum amounts where date is today
        # NOTE: This assumes your table is named 'expenses' and has 'amount' and 'date' columns.
        # If your DB schema is different, this query might need tweaking.
        cursor.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (f"{today}%",))
        result = cursor.fetchone()[0]
        conn.close()
        
        spent = result if result else 0.0
        return f"{RED}£{spent:.2f} Spent Today{RESET}"
    except Exception as e:
        return f"{RED}DB Error (Check Schema){RESET}"

def main():
    os.system('clear')
    os.system('fastfetch --logo none') # <-- MODIFIED LINE
    print("")
    
    # Header
    greeting = get_greeting()
    user = os.environ.get('USER', 'Lukas')
    date_str = datetime.now().strftime("%A, %d %B %Y")
    
    print(f"{BOLD}{CYAN}┌──────────────────────────────────────────────┐{RESET}")
    print(f"{BOLD}{CYAN}│ {greeting}, {user}!                         │{RESET}")
    print(f"{BOLD}{CYAN}│ {date_str:<36}         |{RESET}")
    print(f"{BOLD}{CYAN}└──────────────────────────────────────────────┘{RESET}")
    print("")

    
    # Stats Grid
    print(f" {BOLD}STATUS REPORT:{RESET}")
    print(f" -----------------")
    print(f" 💾 System:    {get_system_stats()}")
    print(f" 📝 Tasks:     {get_pending_tasks()}")
    print(f" 💸 Budget:    {get_todays_spending()}")
    print("")
    print(f"{CYAN}Ready for command... ({RESET}v{VERSION}{CYAN}){RESET}")
    print("")

if __name__ == "__main__":
    main()

