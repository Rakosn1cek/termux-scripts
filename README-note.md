Termux CLI Note Manager (note) v1.1.0
A simple, fast, and robust command-line interface for managing notes directly within your Termux environment. This application uses Python to store and retrieve notes as sequential text files in a dedicated local directory, eliminating the need for cloud services or external dependencies.
Features
 * Zero Setup: No database, no API keys, just local files.
 * Simple Management: Use commands like add, list, edit, view, and delete.
 * Editor Integration: Uses your default $EDITOR (or nano) for editing.
 * Pager Support: Uses less for viewing long notes without cluttering the terminal.
🚀 Installation & Setup
 * Ensure Python is installed:
   pkg install python

 * Save the Script: Place note.py in your executable scripts directory (e.g., ~/termux-scripts/):
   mkdir -p ~/termux-scripts
# [Copy the note.py file content here]
chmod +x ~/termux-scripts/note.py

 * Create the Storage Directory: Notes are stored here.
   mkdir -p ~/notes

 * Create an Alias (Optional, but recommended for easy use):
   Add the following line to your shell configuration file (e.g., ~/.zshrc or ~/.bashrc):
   alias note='python ~/termux-scripts/note.py'

   Then run source ~/.zshrc (or .bashrc).
📋 Usage
The note script uses subcommands to perform actions.
| Command | Action | Example |
|---|---|---|
| add | Creates a new note with the specified content. | note add "Review project proposal by Friday." |
| list | Shows all notes with IDs, creation time, and a preview. | note list |
| view | Shows the full content of a note using the less pager. | note view 3 |
| edit | Opens the note in your default text editor (e.g., nano). | note edit 1 |
| delete | Permanently deletes a note by ID. | note delete 2 |
Example Workflow
# 1. Add a note
$ note add "Need to install Node.js and check the system path setup."
✅ Note added successfully with ID: 1

# 2. List all notes
$ note list
--- LOCAL TERMUX NOTES ---
ID: 1    | 2025-11-30 21:30 | Need to install Node.js and check the system path setup.

# 3. Edit the note
$ note edit 1 
# nano opens... edit and save the file
✅ Note ID 1 edited.

# 4. View the full content
$ note view 1 
# Opens note in less for scrolling


