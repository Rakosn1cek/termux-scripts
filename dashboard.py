#!/usr/bin/env python3
import os
import sqlite3
import json
import shutil
import sys 
from datetime import datetime
VERSION= "1.3.1" #<<-- Fixed daily and recurring expenses display and data pulling from Budget Buddy(expense manager)

# --- Configuration & Paths ---
BUDGET_DB = os.path.expanduser("~/Budget-Buddy-TUI/expenses.db")
TASKS_JSON = os.path.expanduser("~/rich-task-manager-tui/tasks.json")
NOTES_DB_FILE = os.path.expanduser("~/.notes_db.json")

# --- FINAL CONFIRMED CONFIGURATION ---
# Both totals now rely on the 'transactions' table
EXPENSE_TABLE_NAME = "transactions" 
EXPENSE_DATE_COLUMN = "date"    
RECURRING_FLAG = "Recurring payment:" # The unique string used in the description
# ---------------------------------------------

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
    try:
        total, used, free = shutil.disk_usage(os.path.expanduser("~"))
        free_gb = free // (2**30)
        return f"{free_gb} GB Free"
    except Exception:
        return "N/A"

def get_pending_tasks():
    if not os.path.exists(TASKS_JSON):
        return f"{RED}Task file not found{RESET}"
    
    try:
        with open(TASKS_JSON, 'r') as f:
            tasks = json.load(f)
            pending = 0
            for task in tasks:
                is_done = task.get('completed', False) or task.get('status') == 'done'
                if not is_done:
                    pending += 1
            return f"{YELLOW}{pending} Pending{RESET}"
    except Exception:
        return f"{RED}Error reading tasks{RESET}"

def get_todays_spending():
    """
    Calculates the total discretionary (one-off) spending for today.
    Uses the confirmed 'YYYY-MM-DD' date format.
    """
    if not os.path.exists(BUDGET_DB):
        return 0.0, None 
    
    conn = None
    try:
        conn = sqlite3.connect(BUDGET_DB)
        cursor = conn.cursor()
        
        # Confirmed date format is YYYY-MM-DD
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Query: Sum all amounts for today, excluding transactions that are flagged as recurring payments 
        # (to show only today's *new* spending)
        query = f"""
        SELECT SUM(amount) FROM {EXPENSE_TABLE_NAME} 
        WHERE {EXPENSE_DATE_COLUMN} LIKE ? 
          AND description NOT LIKE ?
        """
        search_term = f"{today}%"
        
        # The NOT LIKE is used to exclude the recurring items from the daily total
        cursor.execute(query, (search_term, f"%{RECURRING_FLAG}%"))
        
        result = cursor.fetchone()[0]
        # Only include expenses (positive amounts) if Budget Buddy stores income as negative, or vice versa.
        # Assuming all transactions are stored as positive amounts for simplicity for now.
        spent = result if result is not None else 0.0
        
        return spent, None 
    
    except sqlite3.OperationalError:
        return 0.0, f"{RED}DB ERROR: Daily spending schema error.{RESET}"
    except Exception:
        return 0.0, f"{RED}Error reading daily spending{RESET}"
        
    finally:
        if conn:
            conn.close()

def get_recurring_budget():
    """
    Calculates the total value of all transactions that are flagged as recurring payments.
    NOTE: This is the historical total of applied recurring payments, not a separate template total.
    """
    if not os.path.exists(BUDGET_DB):
        return 0.0, None

    conn = None 
    try:
        conn = sqlite3.connect(BUDGET_DB)
        cursor = conn.cursor()
        
        # The key fix: Query the 'transactions' table and filter by the description field.
        query = f"""
        SELECT SUM(amount) FROM {EXPENSE_TABLE_NAME} 
        WHERE description LIKE ?
        """
        
        # Use LIKE with wildcards to find "Recurring payment: XXXX"
        cursor.execute(query, (f"%{RECURRING_FLAG}%",))
        
        result = cursor.fetchone()[0]
        total_recurring = result if result is not None else 0.0
        
        return total_recurring, None
        
    except sqlite3.OperationalError as e:
        # This will catch errors if the 'transactions' table is still problematic
        return 0.0, f"{RED}Recurring DB Error (Transactions Table): {e}{RESET}"
    except Exception:
        return 0.0, f"{RED}Error reading recurring budget{RESET}"
        
    finally:
        if conn:
            conn.close()

def get_budget_status():
    """Combines and formats the output for both daily spending and recurring budget."""
    
    # NOTE: Daily spending now EXCLUDES recurring payments, 
    # as recurring total includes them separately.
    daily_spent, daily_error = get_todays_spending() 
    recurring_total, recurring_error = get_recurring_budget()

    if not os.path.exists(BUDGET_DB):
        return f"{RED}Budget DB not found{RESET}"

    if daily_error:
        return daily_error 
    if recurring_error:
        return recurring_error

    daily_str = f"£{daily_spent:.2f} Today"
    recurring_str = f"£{recurring_total:.2f} Total Recurring"
    
    return f"{RED}{daily_str}{RESET} | {GREEN}{recurring_str}{RESET}"


def get_note_stats():
    """
    Reads the notes database and returns summary statistics for the dashboard line.
    (Function remains unchanged)
    """
    try:
        if not os.path.exists(NOTES_DB_FILE):
            return f"(0, 0, 'N/A'){RESET}"

        with open(NOTES_DB_FILE, 'r') as f:
            notes = json.load(f)
        
        total_notes = len(notes)
        all_tags = set()
        
        notes_sorted = sorted(notes, 
                              key=lambda x: x.get('created_at', '1900-01-01'), 
                              reverse=True)
        
        most_recent_title = notes_sorted[0].get('title', 'Untitled') if notes_sorted else 'N/A'

        for note in notes:
            if 'tags' in note and note['tags']:
                for tag in note['tags']:
                    all_tags.add(tag.lower())

        unique_tags = len(all_tags)
        
        return f"({total_notes}, {unique_tags}, '{most_recent_title}')"

    except json.JSONDecodeError:
        print(f"{RED}Warning: Notes database is corrupted.{RESET}", file=sys.stderr)
        return f"({RED}0, 0, 'Corrupted DB'{RESET})"
    except Exception:
        return f"({RED}Error{RESET})"
        
def main():
    os.system('clear')
    
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
    print(f" 📚 Notes:     {get_note_stats()}") 
    # Calling the new combined status function
    print(f" 💸 Budget:    {get_budget_status()}") 
    print("")
    print(f"{CYAN}Ready for command... ({RESET}v{VERSION}{CYAN}){RESET}")
    print("")


if __name__ == "__main__":
    main()
