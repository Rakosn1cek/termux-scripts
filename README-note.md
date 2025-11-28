🧠 Simple Note Taking App (note.py) v1.0.0

A lightweight, command-line utility for managing personal notes, quick thoughts, and code snippets directly from the terminal. It uses a simple JSON database (~/.notes_db.json) for persistence.
✨ Features
 * Title & Description: Store key context (Title) and detailed content (Description).
 * Creation Date: Automatically tracks when each note was created.
 * Tagging: Organize notes using searchable tags (e.g., code, shopping, todo).
 * CRUD Operations: Full support for Create, Read (View/List), Update (Edit), and Delete.
 * Filtering: List notes by a specific tag.
 * Editor Integration: Uses your shell's $EDITOR (e.g., nano or vim) for clean editing.
🚀 Setup
1. File Location
Ensure the note.py script is saved in a convenient location, such as your home directory:
# Assuming you created the file in your home directory
cd ~
chmod +x note.py

2. Create an Alias (Recommended)
To run the script easily by just typing note, add the following alias to your shell's configuration file (~/.zshrc or ~/.bashrc):
nano ~/.zshrc

Add this line:
alias note="python3 ~/note.py"

Save and exit, then reload your shell configuration:
source ~/.zshrc

💡 Usage Examples
All commands are executed using the alias note.
1. Adding a Note (add)
The title is the first argument, and the description (content) is passed using the -c or --content flag. Tags are optional.
| Action | Command |
|---|---|
| Basic Add | note add "Daily Goals" -c "Finish report, call client, buy milk" |
| With Tags | note add "Bash Script Trick" -c "Use 'set -e' for error checking." -t code bash cli |
2. Listing Notes (list)
List all notes or filter by a specific tag.
| Action | Command |
|---|---|
| List All | note list |
| Filter by Tag | note list --tag code |
3. Viewing a Note (view)
View the full content and metadata for a specific note ID.
| Action | Command |
|---|---|
| View Note | note view 5 |
4. Editing a Note (edit)
Opens the note's content in your terminal editor (nano or vim).
| Action | Command |
|---|---|
| Edit Content | note edit 5 |
5. Managing Tags (tag add, tag remove)
Add or remove tags from an existing note.
| Action | Command |
|---|---|
| Add a Tag | note tag add 5 urgent |
| Remove a Tag | note tag remove 5 bash |
6. Deleting a Note (delete)
Permanently removes a note after asking for confirmation.
| Action | Command |
|---|---|
| Delete Note | note delete 2 |

