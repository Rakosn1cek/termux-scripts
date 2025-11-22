# Termux Knowledge Base (KB) Utility

A simple, command-line utility built in Python to save, search, and manage quick code snippets, technical notes, and helpful commands directly within the Termux terminal environment.

## 🚀 Setup and Installation

1.  **File Location:** Ensure `kb.py` is saved in the `~/termux-scripts` directory.
2.  **Database:** The notes are stored in `~/.kb_data.json`.
3.  **Alias:** To run the script simply by typing `kb`, add the following alias to your `~/.zshrc` file:

    ```bash
    alias kb="python3 ~/termux-scripts/kb.py"
    ```

## ✨ Core Features

| Command | Description |
| :--- | :--- |
| `kb add` | Adds a new note with a title, content, and optional tags. |
| `kb list` | Lists the IDs and titles of all stored notes. |
| `kb search <query>` | Searches notes by title, content, or tags. |
| `kb view <ID>` | Displays a note's full content cleanly. |
| `kb edit <ID>` | Opens the note's content in the user's `$EDITOR` (e.g., Nano/Vim) for quick modification. |
| `kb delete <ID>` | Permanently deletes a note after confirmation. |
| `kb tag add/remove` | Manages tags on an existing note. |

## 💡 Usage Examples

```bash
# 1. Add a quick note about a Termux path
kb add "Termux Path Variable" -c "The home directory is /data/data/com.termux/files/home" -t termux path

# 2. View the full content of note ID 5
kb view 5

# 3. Add a tag to an existing note
kb tag add 5 important

# 4. Search the database for any entries containing 'termux'
kb search termux

