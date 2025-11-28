#!/usr/bin/env python3
import argparse
import json
import os
import sys
from datetime import datetime
import uuid
import subprocess

# --- Configuration & Paths ---
DB_FILE = os.path.expanduser("~/.notes_db.json")

# Colors (Adjust these if not running in Termux/Zsh)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# --- Database Handling ---
def load_db():
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"{RED}Warning: Database file is corrupted. Starting with an empty list.{RESET}")
        return []
    except Exception as e:
        print(f"{RED}Unexpected error loading DB: {e}{RESET}")
        return []

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- Helper Functions ---
def print_note(note, full_content=False):
    tags_str = f" ({', '.join(note.get('tags', []))})" if note.get('tags') else ""
    print(f"[{note['id']}] {BOLD}{note['title']}{RESET} {YELLOW}{tags_str}{RESET}")
    print(f"  {CYAN}Created:{RESET} {note['created_at']}")
    
    if full_content:
        print(f"\n{BOLD}--- Description ---{RESET}")
        print(note['content'])
        print("-" * 20)

def generate_id(db):
    if not db:
        return 1
    # Find the maximum existing ID and increment it
    return max(n['id'] for n in db) + 1

# --- Command Functions ---

def add_note(args):
    db = load_db()
    
    # Check for title and description input
    if not args.title or not args.content:
        print(f"{RED}Error: Title and description (-c) are required.{RESET}")
        return

    new_id = generate_id(db)
    
    new_note = {
        'id': new_id,
        'title': args.title,
        'content': args.content,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'tags': [tag.lower() for tag in args.tags] if args.tags else []
    }
    
    db.append(new_note)
    save_db(db)
    print(f"✅ {GREEN}Note ID {new_id} ('{args.title}') added successfully.{RESET}")


def list_notes(args):
    db = load_db()
    
    if not db:
        print("No notes found.")
        return
    
    # Apply filtering if a tag is provided
    if args.tag:
        tag_query = args.tag.lower()
        filtered_db = [
            note for note in db
            if tag_query in [t.lower() for t in note.get('tags', [])]
        ]
    else:
        filtered_db = db

    if not filtered_db:
        tag_info = f" with tag '{args.tag}'" if args.tag else ""
        print(f"{RED}No notes found{tag_info}.{RESET}")
        return

    tag_info = f" (Tag Filter: {args.tag})" if args.tag else ""
    print(f"\n{BOLD}{CYAN}--- Notes Found ({len(filtered_db)}){tag_info} ---{RESET}")
    for note in filtered_db:
        print_note(note, full_content=False)
        print("-" * 20)


def view_note(args):
    db = load_db()
    try:
        note = next(n for n in db if n['id'] == args.id)
        print_note(note, full_content=True)
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")


def edit_note(args):
    db = load_db()
    
    try:
        note = next(n for n in db if n['id'] == args.id)
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")
        return
        
    editor = os.environ.get('EDITOR', 'nano') # Use nano as default editor
    
    # 1. Create a temporary file with the current content
    temp_file_name = f"/tmp/note_edit_{note['id']}_{uuid.uuid4()}.txt"
    try:
        with open(temp_file_name, 'w') as f:
            f.write(note['content'])
        
        # 2. Open the editor
        subprocess.run([editor, temp_file_name])
        
        # 3. Read the modified content
        with open(temp_file_name, 'r') as f:
            new_content = f.read().strip()
            
        # 4. Check if content changed
        if new_content == note['content']:
            print(f"{YELLOW}Note ID {args.id}: Content unchanged. Edit cancelled.{RESET}")
            return
            
        # 5. Update the note in the database
        note['content'] = new_content
        save_db(db)
        print(f"✅ {GREEN}Note ID {args.id} content updated successfully.{RESET}")
        
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_name):
            os.remove(temp_file_name)


def delete_note(args):
    db = load_db()
    
    try:
        note = next(n for n in db if n['id'] == args.id)
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")
        return

    print(f"\n{YELLOW}--- CONFIRM DELETION ---{RESET}")
    print(f"Are you sure you want to delete Note ID {note['id']} ('{note['title']}')?")
    
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        new_db = [n for n in db if n['id'] != args.id]
        save_db(new_db)
        print(f"✅ {GREEN}Note ID {args.id} successfully DELETED.{RESET}")
    else:
        print(f"{CYAN}Deletion cancelled.{RESET}")


def tag_management(args):
    db = load_db()
    
    try:
        note = next(n for n in db if n['id'] == args.id)
    except StopIteration:
        print(f"{RED}Error: Note with ID {args.id} not found.{RESET}")
        return

    current_tags = set(note.get('tags', []))
    tag_name = args.tag.lower()
    
    if args.action == 'add':
        if tag_name in current_tags:
            print(f"{YELLOW}Tag '{tag_name}' already exists on Note ID {args.id}.{RESET}")
            return
        
        current_tags.add(tag_name)
        note['tags'] = sorted(list(current_tags))
        save_db(db)
        print(f"✅ {GREEN}Tag '{tag_name}' added to Note ID {args.id}.{RESET}")
        
    elif args.action == 'remove':
        if tag_name not in current_tags:
            print(f"{YELLOW}Tag '{tag_name}' not found on Note ID {args.id}.{RESET}")
            return
        
        current_tags.remove(tag_name)
        note['tags'] = sorted(list(current_tags))
        save_db(db)
        print(f"✅ {GREEN}Tag '{tag_name}' removed from Note ID {args.id}.{RESET}")


# --- Main Logic ---

def main():
    parser = argparse.ArgumentParser(
        description="Simple Note Taking App",
        epilog="Usage: note.py add 'Title' -c 'Description' -t tag1 tag2"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'add' command (Title, Description, Tags, Creation Date handled internally)
    parser_add = subparsers.add_parser("add", help="Add a new note")
    parser_add.add_argument("title", type=str, help="Title of the note")
    parser_add.add_argument("-c", "--content", required=True, type=str, help="Description/Content of the note")
    parser_add.add_argument("-t", "--tags", nargs='*', type=str, help="Optional tags for organization")
    parser_add.set_defaults(func=add_note)

    # 'list' command (with optional tag filter)
    parser_list = subparsers.add_parser("list", help="List all notes (IDs, Titles, Creation Date)")
    parser_list.add_argument("-t", "--tag", type=str, help="Filter notes by a specific tag", default=None)
    parser_list.set_defaults(func=list_notes)

    # 'view' command
    parser_view = subparsers.add_parser("view", help="View a single note's full description")
    parser_view.add_argument("id", type=int, help="ID of the note to view")
    parser_view.set_defaults(func=view_note)

    # 'edit' command
    parser_edit = subparsers.add_parser("edit", help="Edit a note's content using $EDITOR")
    parser_edit.add_argument("id", type=int, help="ID of the note to edit")
    parser_edit.set_defaults(func=edit_note)

    # 'delete' command
    parser_delete = subparsers.add_parser("delete", help="Delete a note by ID")
    parser_delete.add_argument("id", type=int, help="ID of the note to delete")
    parser_delete.set_defaults(func=delete_note)

    # 'tag' parent command
    parser_tag = subparsers.add_parser("tag", help="Manage tags on a note")
    tag_subparsers = parser_tag.add_subparsers(dest="action", required=True)

    # 'tag add' command
    parser_tag_add = tag_subparsers.add_parser("add", help="Add a tag to a note")
    parser_tag_add.add_argument("id", type=int, help="ID of the note")
    parser_tag_add.add_argument("tag", type=str, help="Tag name to add")
    parser_tag_add.set_defaults(func=tag_management)

    # 'tag remove' command
    parser_tag_remove = tag_subparsers.add_parser("remove", help="Remove a tag from a note")
    parser_tag_remove.add_argument("id", type=int, help="ID of the note")
    parser_tag_remove.add_argument("tag", type=str, help="Tag name to remove")
    parser_tag_remove.set_defaults(func=tag_management)

    # Parse arguments and call function defined by set_defaults
    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()

