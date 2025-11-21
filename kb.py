#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime

# --- Configuration ---
DB_FILE = os.path.expanduser("~/.kb_data.json")
# Colors for Termux
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

# --- Database Handling ---
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Helper: Print Note ---
def print_note(note):
    print(f"{CYAN}ID: {note['id']} | {note['date']}{RESET}")
    print(f"{GREEN}Title: {note['title']}{RESET}")
    if note['content']:
        print(f"Content: {note['content']}")
    if note['tags']:
        print(f"{YELLOW}Tags: {', '.join(note['tags'])}{RESET}")
    print("-" * 30)

# --- Commands ---
def add_note(args):
    db = load_db()
    new_id = 1 if not db else db[-1]['id'] + 1
    
    new_note = {
        "id": new_id,
        "title": args.title,
        "content": args.content, 
        "tags": args.tags,       
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    db.append(new_note)
    save_db(db)
    print(f"✅ {GREEN}Note added! [ID: {new_id}]{RESET}")

def list_notes(args):
    db = load_db()
    if not db:
        print("No notes found.")
        return
    
    print(f"\n{CYAN}--- All Notes ({len(db)}) ---{RESET}")
    for note in db:
        print(f"[{note['id']}] {note['title']} {YELLOW}({', '.join(note['tags'])}){RESET}")

def search_notes(args):
    db = load_db()
    query = args.query.lower()
    found = False
    
    print(f"\n{CYAN}--- Search Results for '{query}' ---{RESET}")
    for note in db:
        # Search in title, content, and tags
        in_title = query in note['title'].lower()
        in_content = query in note['content'].lower() if note['content'] else False
        in_tags = any(query in tag.lower() for tag in note['tags'])
        
        if in_title or in_content or in_tags:
            print_note(note)
            found = True
            
    if not found:
        print(f"{RED}No matches found.{RESET}")

# --- Main CLI Setup ---
def main():
    parser = argparse.ArgumentParser(description="Termux Knowledge Base (kb)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command
    parser_add = subparsers.add_parser("add", help="Add a new note")
    parser_add.add_argument("title", type=str, help="Title of the note")
    parser_add.add_argument("-c", "--content", type=str, help="Code snippet or body", default="")
    parser_add.add_argument("-t", "--tags", nargs="+", help="Tags", default=[])

    # 'list' command
    parser_list = subparsers.add_parser("list", help="List all notes")

    # 'search' command
    parser_search = subparsers.add_parser("search", help="Search notes")
    parser_search.add_argument("query", type=str, help="Search term")

    args = parser.parse_args()

    if args.command == "add":
        add_note(args)
    elif args.command == "list":
        list_notes(args)
    elif args.command == "search":
        search_notes(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
