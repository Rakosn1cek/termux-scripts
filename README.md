# Termux Knowledge Base (KB) Utility v1.1.0

A command-line utility built in Python to save, search, and manage quick code snippets and notes directly within the Termux terminal environment.

## 🚀 Setup and Installation

1.  **File Location:** Ensure `kb.py` is saved in the `~/termux-scripts` directory.
2.  **Database:** The notes are stored in `~/.kb_data.json`.
3.  **Alias:** To run the script simply by typing `kb`, add the following alias to your `~/.zshrc` file:

    ```bash
    alias kb="python3 ~/termux-scripts/kb.py"
    ```

## ✨ Core Features (v1.1.0)

| Command | Description |
| :--- | :--- |
| `kb add` | Adds a new note with a title, content, and optional tags. |
| `kb list` | Lists all notes. |
| `kb list --tag <tag>` | **New:** Filters the list to show only notes with the specified tag. |
| `kb search <query>` | Performs a general search across titles, content, and tags. |
| `kb search <query> --tag` | **New:** Searches for the query exclusively within note tags. |
| `kb view <ID>` | Displays a note's full content cleanly. |
| `kb edit <ID>` | Opens content in the user's `$EDITOR` (e.g., Nano/Vim) for modification. |
| `kb delete <ID>` | Permanently deletes a note after confirmation. |
| `kb tag add/remove` | Manages tags on an existing note. |
| `kb --version` | Displays the current script version. |

## 💡 Usage Examples

```bash
# 1. Add a new note with tags
kb add "Fix Git Auth" -c "Use PAT instead of password when pushing on Termux." -t git termux

# 2. List all notes with the tag 'git'
kb list --tag git

# 3. Search exclusively for the tag 'termux'
kb search termux --tag

# 4. View the full content of note ID 5
kb view 5

# 5. Delete note ID 12
kb delete 12

