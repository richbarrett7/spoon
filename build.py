import os
import shutil
import time
import hashlib
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

SRC_DIR = "src"
PUBLIC_DIR = "public"

def generate_cachebust():
    """Generate a hash based on the current timestamp (including microseconds)."""
    timestamp = datetime.utcnow().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:10]  # Shortened hash

def load_includes():
    """Load all include files from src/ into a dictionary with full relative paths."""
    include_files = {}
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".include.html"):
                rel_path = os.path.relpath(os.path.join(root, file), SRC_DIR)  # Keep relative path
                with open(os.path.join(root, file), encoding="utf-8") as f:
                    include_files[rel_path] = f.read()
    return include_files

def build():
    """Copies HTML files and processes includes with cache busting."""
    print("🔄 Rebuilding site...")

    # Ensure public directory exists
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    # Generate a new cache busting value for each build
    cachebust_value = generate_cachebust()

    # Load include files from all subdirectories
    include_files = load_includes()

    # Copy and process HTML files
    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if file.endswith(".html") and not file.endswith(".include.html"):
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, SRC_DIR)  # Keep relative path
                dest_path = os.path.join(PUBLIC_DIR, rel_path)

                # Ensure the destination subdirectory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Copy file first
                shutil.copy(src_path, dest_path)

                # Read copied file
                with open(dest_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Replace placeholders in the copied file
                for inc_path, inc_content in include_files.items():
                    placeholder = f"{{{{ {inc_path} }}}}"  # Matches exact relative path
                    content = content.replace(placeholder, inc_content)

                # Replace cachebust placeholder
                content = content.replace("{{ cachebust }}", cachebust_value)

                # Write modified content back to the copied file
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(content)

    print(f"✅ Build complete! Cachebust: {cachebust_value}\n")


class ChangeHandler(FileSystemEventHandler):
    """Handles file changes in the src directory."""

    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"🔄 Detected change: {event.event_type.upper()} → {event.src_path}")
        build()


if __name__ == "__main__":
    # Initial build
    build()

    # Start file watcher
    observer = Observer()
    observer.schedule(ChangeHandler(), path=SRC_DIR, recursive=True)
    observer.start()

    print(f"👀 Watching for changes in {SRC_DIR} and subdirectories...\n")
    
    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
