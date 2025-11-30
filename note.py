import argparse
import os
import subprocess
import sys
from datetime import datetime

# --- CONFIGURATION ---
# Notes will be stored as individual text files in this folder.
NOTES_DIR = os.path.expanduser("~/notes")
PREVIEW_CHAR_LIMIT = 80  # Increased from 50
# ---------------------

def get_next_id():
    """Finds the next available sequential ID based on existing files."""
    try:
        if not os.path.exists(NOTES_DIR):
            return 1
            
        existing_ids = []
        for filename in os.listdir(NOTES_DIR):
            if filename.endswith(".txt"):
                try:
                    # Filename is the ID (e.g., '5.txt' -> 5)
                    existing_ids.append(int(os.path.splitext(filename)[0]))
                except ValueError:
                    # Ignore files that are not numbered notes
                    continue
        
        # Return the next highest ID or 1 if no files exist
        return max(existing_ids) + 1 if existing_ids else 1
    
    except Exception as e:
        print(f"Error determining next ID: {e}", file=sys.stderr)
        return 1

def get_note_filepath(note_id):
    """Returns the full path for a given note ID."""
    return os.path.join(NOTES_DIR, f"{note_id}.txt")

def add_note(args):
    """Adds a new note by creating a new file."""
    if not os.path.exists(NOTES_DIR):
        os.makedirs(NOTES_DIR)
        
    new_id = get_next_id()
    filepath = get_note_filepath(new_id)
    
    try:
        with open(filepath, 'w') as f:
            f.write(args.content.strip())
            f.write(f"\n\n# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"✅ Note added successfully with ID: {new_id}")
    except Exception as e:
        print(f"Error saving note: {e}", file=sys.stderr)

def edit_note(args):
    """Opens an existing note file in the default editor (nano)."""
    note_id = args.id
    filepath = get_note_filepath(note_id)

    if not os.path.exists(filepath):
        print(f"Error: Note with ID '{note_id}' not found at {filepath}.", file=sys.stderr)
        return

    # Check if EDITOR environment variable is set, otherwise default to nano
    editor = os.environ.get('EDITOR', 'nano')
    
    try:
        # Open the editor directly on the note file
        subprocess.run([editor, filepath], check=True)
        print(f"✅ Note ID {note_id} edited.")
    except subprocess.CalledProcessError:
        print("Editor failed or was closed improperly.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred during editing: {e}", file=sys.stderr)

# --- NEW FUNCTION FOR VIEWING ---
def view_note(args):
    """Views the full content of a note using a pager (like less)."""
    note_id = args.id
    filepath = get_note_filepath(note_id)

    if not os.path.exists(filepath):
        print(f"Error: Note with ID '{note_id}' not found.", file=sys.stderr)
        return

    # Use 'less' as the default pager for viewing long content
    pager = os.environ.get('PAGER', 'less')
    
    try:
        # Pass the file directly to the pager for easy scrolling
        subprocess.run([pager, filepath], check=True)
    except Exception as e:
        print(f"Error viewing note: {e}", file=sys.stderr)
# --------------------------------

def list_notes(args):
    """Lists all notes with their IDs and content previews."""
    if not os.path.exists(NOTES_DIR):
        print("No notes directory found. Use 'note add' to start.")
        return

    print("\n--- LOCAL TERMUX NOTES ---")
    found = False
    
    for filename in sorted(os.listdir(NOTES_DIR), key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else 0):
        if filename.endswith(".txt"):
            try:
                note_id = os.path.splitext(filename)[0]
                filepath = get_note_filepath(note_id)
                
                with open(filepath, 'r') as f:
                    content = f.read()

                # Get the modification time
                mod_time = os.path.getmtime(filepath)
                time_str = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
                
                # Use the first line of content for the preview
                first_line = content.split('\n')[0].strip()
                preview = first_line[:PREVIEW_CHAR_LIMIT]
                
                if len(first_line) > PREVIEW_CHAR_LIMIT:
                    preview += '...'
                
                print(f"ID: {note_id.ljust(4)} | {time_str} | {preview}")
                found = True

            except Exception as e:
                print(f"Error processing file {filename}: {e}", file=sys.stderr)
                
    if not found:
        print("No notes found. Use 'note add \"My first note\"' to start.")
    else:
        print("\nUse 'note view [id]' to see the full content.")
    print("--------------------------")

def delete_note(args):
    """Deletes a note file."""
    note_id = args.id
    filepath = get_note_filepath(note_id)

    if not os.path.exists(filepath):
        print(f"Error: Note with ID '{note_id}' not found.", file=sys.stderr)
        return

    try:
        os.remove(filepath)
        print(f"🗑️ Note ID {note_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting note file: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Termux Note Management CLI (Local File Storage).")
    
    # Subparsers for commands (add, list, edit, delete, view)
    subparsers = parser.add_subparsers(dest='command', required=True)

    # --- Add Command ---
    parser_add = subparsers.add_parser('add', help='Add a new note.')
    parser_add.add_argument('content', type=str, help='The content of the new note.')
    parser_add.set_defaults(func=add_note)

    # --- Edit Command ---
    parser_edit = subparsers.add_parser('edit', help='Edit an existing note by ID.')
    parser_edit.add_argument('id', type=int, help='The ID of the note to edit.')
    parser_edit.set_defaults(func=edit_note)
    
    # --- View Command (New) ---
    parser_view = subparsers.add_parser('view', help='View the full content of a note by ID using a pager.')
    parser_view.add_argument('id', type=int, help='The ID of the note to view.')
    parser_view.set_defaults(func=view_note)

    # --- List Command ---
    parser_list = subparsers.add_parser('list', help='List all notes.')
    parser_list.set_defaults(func=list_notes)
    
    # --- Delete Command ---
    parser_delete = subparsers.add_parser('delete', help='Delete an existing note by ID.')
    parser_delete.add_argument('id', type=int, help='The ID of the note to delete.')
    parser_delete.set_defaults(func=delete_note)


    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
