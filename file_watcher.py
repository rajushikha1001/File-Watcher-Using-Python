import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the log file
log_file = 'changes.log'

# Set up the logging configuration
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Define the event handler class
class WatcherHandler(FileSystemEventHandler):
    def __init__(self, ignore_extensions=None, ignore_folders=None):
        self.ignore_extensions = ignore_extensions if ignore_extensions else []
        self.ignore_folders = ignore_folders if ignore_folders else []

    def _should_ignore(self, path):
        # Check if the file has an extension to ignore
        if any(path.endswith(ext) for ext in self.ignore_extensions):
            return True

        # Check if the file is in a folder to ignore
        if any(folder in path for folder in self.ignore_folders):
            return True

        return False

    def on_modified(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            logging.info(f"Modified file: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            logging.info(f"Created file: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory and not self._should_ignore(event.src_path):
            logging.info(f"Deleted file: {event.src_path}")

# Function to watch a directory
def watch_directory(path_to_watch, ignore_extensions=None, ignore_folders=None):
    event_handler = WatcherHandler(ignore_extensions=ignore_extensions, ignore_folders=ignore_folders)
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    
    logging.info(f"Started watching directory: {path_to_watch}")
    observer.start()
    
    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()  # Stop the observer on keyboard interrupt
        logging.info("Stopped watching directory.")
    observer.join()    

if __name__ == "__main__":
    # Specify the directory to watch
    path_to_watch = input("Enter the path of the directory to watch: ")
    watch_directory(path_to_watch)
