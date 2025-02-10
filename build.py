import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import hashlib
from datetime import datetime

SRC_DIR = "src"
PUBLIC_DIR = "public"

def generate_cachebust():
    """Generate a hash based on the current timestamp (including microseconds)."""
    timestamp = datetime.utcnow().isoformat()
    return hashlib.md5(timestamp.encode()).hexdigest()[:10]  # Shortened hash

def build():
    """Copies HTML files and processes includes with cache busting."""
    print("🔄 Rebuilding site...")

    # Ensure public directory exists
    os.makedirs(PUBLIC_DIR, exist_ok=True)

    # Generate a new cache busting value for each build
    cachebust_value = generate_cachebust()

    # Load include files into a dictionary
    include_files = {
        f: open(os.path.join(SRC_DIR, f), encoding="utf-8").read()
        for f in os.listdir(SRC_DIR) if f.endswith(".include.html")
    }

    # Copy and process HTML files
    for filename in os.listdir(SRC_DIR):
        if filename.endswith(".html") and not filename.endswith(".include.html"):
            src_path = os.path.join(SRC_DIR, filename)
            dest_path = os.path.join(PUBLIC_DIR, filename)

            # Copy file first
            shutil.copy(src_path, dest_path)

            # Read copied file
            with open(dest_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace placeholders in the copied file
            for inc_file, inc_content in include_files.items():
                placeholder = f"{{{{ {inc_file} }}}}"
                content = content.replace(placeholder, inc_content)

            # Replace cachebust placeholder
            content = content.replace("{{ cachebust }}", cachebust_value)

            # Write modified content back to the copied file
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

    print(f"✅ Build complete! Cachebust: {cachebust_value}\n")


class ChangeHandler(FileSystemEventHandler):
    """Handles file changes in the src directory."""

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"📝 Modified: {event.src_path}")
        build()

    def on_created(self, event):
        if event.is_directory:
            return
        print(f"➕ Created: {event.src_path}")
        build()

    def on_deleted(self, event):
        if event.is_directory:
            return
        print(f"❌ Deleted: {event.src_path}")
        build()

    def on_moved(self, event):
        if event.is_directory:
            return
        print(f"🔀 Moved: {event.src_path} → {event.dest_path}")
        build()


if __name__ == "__main__":
    # Initial build
    build()

    # Start file watcher
    observer = Observer()
    observer.schedule(ChangeHandler(), path=SRC_DIR, recursive=False)
    observer.start()

    print(f"👀 Watching for changes in {SRC_DIR}...\n")
    
    try:
        while True:
            time.sleep(1)  # Keep script running
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
