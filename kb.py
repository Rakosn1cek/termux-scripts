#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
from datetime import datetime
import tempfile
import sys
VERSION= "1.1.0"

# --- Configuration & Paths ---
DB_FILE = os.path.expanduser("~/.kb_data.json")

# Define the user's preferred editor (defaults to nano if EDITOR is not set)
EDITOR = os.environ.get('EDITOR', 'nano')

# Colors for Termux
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
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
    # Ensure all integers are saved as integers (especially 'id')
    for item in data:
        if 'id' in item:
            item['id'] = int(item['id'])
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Helper: Print Note ---
def print_note(note, full_content=False):
    print(f"\n{BOLD}{CYAN}┌──────────────────────────────────────────────┐{RESET}")
    print(f"│ {BOLD}ID: {note['id']} | {note['date']} {RESET:<28}│")
    print(f"│ {GREEN}Title: {note['title']}{RESET:<35}│")
    print(f"{CYAN}└──────────────────────────────────────────────┘{RESET}")
    if note.get('tags'):
        print(f"{YELLOW}Tags: {', '.join(note['tags'])}{RESET}")
    
    # Display full content for view command or search
    if note.get('content'):
        print(f"\n{BOLD}CONTENT:{RESET}")
        if full_content:
            print(note['content'])
        else:
             # Truncate content for search/list preview
            content_preview = note['content'][:150] + '...' if len(note['content']) > 150 else note['content']
            print(content_preview)
    print("-" * 50)


# --- New Command: View ---
def view_note(args):
    db = load_db()
    note = next((n for n in db if n['id'] == args.id), None)
    
    if note:
        print_note(note, full_content=True)
    else:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")

# --- New Command: Edit ---
def edit_note(args):
    db = load_db()
    
    # 1. Find the note
    try:
        index = next(i for i, n in enumerate(db) if n['id'] == args.id)
        note = db[index]
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")
        return

    # 2. Use a temporary file to hold the content
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
        # Write the content to be edited
        tmp.write(note['content'])
        tmp_path = tmp.name

    # 3. Call the user's preferred editor
    try:
        print(f"{CYAN}Opening note content in {EDITOR}...{RESET}")
        subprocess.run([EDITOR, tmp_path])
    except FileNotFoundError:
        print(f"{RED}Error: Editor '{EDITOR}' not found. Please check your $EDITOR environment variable.{RESET}")
        os.remove(tmp_path)
        return

    # 4. Read the modified content back
    with open(tmp_path, 'r') as tmp:
        modified_content = tmp.read()

    # 5. Update the database
    if modified_content != note['content']:
        note['content'] = modified_content
        note['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Update timestamp
        save_db(db)
        print(f"✅ {GREEN}Note ID {args.id} updated successfully.{RESET}")
    else:
        print("Note content unchanged.")
        
    # Clean up the temporary file
    os.remove(tmp_path)


# --- Command: Delete ---
def delete_note(args):
    db = load_db()

    # 1. Find the note
    try:
        note = next(n for n in db if n['id'] == args.id)
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")
        return

    print(f"\n{YELLOW}--- CONFIRM DELETION ---{RESET}")
    print(f"Are you sure you want to delete Note ID {note['id']} ({note['title']})?")

    # 2. Ask for confirmation
    confirm = input("Type 'yes' to confirm: ")

    if confirm.lower() == 'yes':
        # 3. Filter the note out of the list
        new_db = [n for n in db if n['id'] != args.id]
        save_db(new_db)
        print(f"✅ {GREEN}Note ID {args.id} and content successfully DELETED.{RESET}")
    else:
        print(f"{CYAN}Deletion cancelled.{RESET}")


# --- Existing Commands (Condensed) ---
def add_note(args):
    db = load_db()
    new_id = 1 if not db else max(n.get('id', 0) for n in db) + 1 # Robust ID generation
    
    new_note = {
        "id": new_id,
        "title": args.title,
        "content": args.content, 
        "tags": args.tags,       
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    db.append(new_note)
    save_db(db)
    print(f"✅ {GREEN}Note added! [ID: {new_id}]{RESET}")

def list_notes(args):
    db = load_db()
    
    # 1. Start with the full database
    filtered_db = db
    
    # 2. Apply filtering if a tag is provided
    if args.tag:
        tag_query = args.tag.lower()
        # Filter notes where the tag_query is present in the note's tags list
        filtered_db = [
            note for note in db
            if tag_query in [t.lower() for t in note.get('tags', [])]
        ]
        
    if not filtered_db:
        if args.tag:
            print(f"{RED}No notes found with tag '{args.tag}'.{RESET}")
        else:
            print("No notes found.")
        return
    
    # 3. Print the results
    tag_info = f" (Tag: {args.tag})" if args.tag else ""
    print(f"\n{BOLD}{CYAN}--- Notes Found ({len(filtered_db)}){tag_info} ---{RESET}")
    for note in filtered_db:
        # Display note information cleanly
        tags_str = f" ({', '.join(note.get('tags', []))})" if note.get('tags') else ""
        print(f"[{note['id']}] {note['title']} {YELLOW}{tags_str}{RESET}")

    
    print(f"\n{BOLD}{CYAN}--- All Notes ({len(db)}) ---{RESET}")
    for note in db:
        print(f"[{note['id']}] {note['title']} {YELLOW}({', '.join(note.get('tags', []))}){RESET}")

def search_notes(args):
    db = load_db()
    query = args.query.lower()
    found = False
    
    # Check if we should only search tags
    tag_only_mode = args.tag_only
    
    print(f"\n{BOLD}{CYAN}--- Search Results for '{query}' ---{RESET}")
    
    for note in db:
        # Check for tag match regardless of mode
        in_tags = any(query in tag.lower() for tag in note.get('tags', []))
        
        if tag_only_mode:
            # Mode 1: Only check tags
            if in_tags:
                print_note(note, full_content=False)
                found = True
        else:
            # Mode 2: Check all fields (standard search)
            in_title = query in note.get('title', '').lower()
            in_content = query in note.get('content', '').lower()
            
            if in_title or in_content or in_tags:
                print_note(note, full_content=False)
                found = True
            
    if not found:
        print(f"{RED}No matches found.{RESET}")

    
    print(f"\n{BOLD}{CYAN}--- Search Results for '{query}' ---{RESET}")
    for note in db:
        # Search logic remains the same
        in_title = query in note.get('title', '').lower()
        in_content = query in note.get('content', '').lower()
        in_tags = any(query in tag.lower() for tag in note.get('tags', []))
        
        if in_title or in_content or in_tags:
            print_note(note, full_content=False)
            found = True
            
    if not found:
        print(f"{RED}No matches found.{RESET}")


# --- Main CLI Setup ---
def main():
    parser = argparse.ArgumentParser(
    description="Termux Knowledge Base (kb)",
    epilog=f"Version: v{VERSION}"
)
    parser.add_argument('--version', action='version', version=f'%(prog)s v{VERSION}')

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'add' command
    parser_add = subparsers.add_parser("add", help="Add a new note")
    parser_add.add_argument("title", type=str, help="Title of the note")
    parser_add.add_argument("-c", "--content", type=str, help="Code snippet or body", default="")
    parser_add.add_argument("-t", "--tags", nargs="+", help="Tags", default=[])
    parser_add.set_defaults(func=add_note)

    # 'list' command
    parser_list = subparsers.add_parser("list", help="List all notes")
    parser_list.add_argument("-t", "--tag", type=str, help="Filter notes by a specific tag", default=None)
    parser_list.set_defaults(func=list_notes)


    # 'search' command
    parser_search = subparsers.add_parser("search", help="Search notes")
    parser_search.add_argument("query", type=str, help="Search term")
    parser_search.add_argument("--tag", dest="tag_only", action="store_true", 
                                help="Search tags exclusively, ignoring title and content.")
    parser_search.set_defaults(func=search_notes)

    
    # 'view' command (NEW)
    parser_view = subparsers.add_parser("view", help="View a specific note by ID")
    parser_view.add_argument("id", type=int, help="ID of the note to view")
    parser_view.set_defaults(func=view_note)
    
    # 'edit' command (NEW)
    parser_edit = subparsers.add_parser("edit", help="Edit a note's content by ID")
    parser_edit.add_argument("id", type=int, help="ID of the note to edit")
    parser_edit.set_defaults(func=edit_note)
    
    # 'delete' command (NEW)
    parser_delete = subparsers.add_parser("delete", help="Delete a note by ID")
    parser_delete.add_argument("id", type=int, help="ID of the note to delete")
    parser_delete.set_defaults(func=delete_note)


    # Parse arguments and call function defined by set_defaults
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
