import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Path to the folder you want to watch (e.g., Downloads)
WATCH_DIR = os.path.expanduser("~/Downloads")

# Mapping of file extensions to folder names
DEST_DIRS = {
    "Documents": [".pdf", ".docx", ".txt", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Audio": [".mp3", ".wav", ".flac"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Code": [".py", ".js", ".html", ".css", ".sh"]
}

class MoveHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(WATCH_DIR):
            file_ext = os.path.splitext(filename)[1].lower()
            
            for folder_name, extensions in DEST_DIRS.items():
                if file_ext in extensions:
                    self.move_file(filename, folder_name)

    def move_file(self, filename, folder_name):
        # Create destination folder if it doesn't exist
        dest_path = os.path.join(WATCH_DIR, folder_name)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        
        # Move the file
        source = os.path.join(WATCH_DIR, filename)
        destination = os.path.join(dest_path, filename)
        
        # Simple collision check: if file exists, don't overwrite
        if not os.path.exists(destination):
            shutil.move(source, destination)
            print(f"Moved: {filename} -> {folder_name}/")

if __name__ == "__main__":
    event_handler = MoveHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    
    print(f"Monitoring: {WATCH_DIR}...")
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
