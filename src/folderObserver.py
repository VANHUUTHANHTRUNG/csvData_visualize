from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import time

patterns = ["*.txt"]
ignore_patterns = ""
ignore_directories = False
case_sensitive = True


class Handler(PatternMatchingEventHandler):
    def on_created(self, event):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{now}---Created: {event.src_path}")

    def on_deleted(self, event):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{now}---Deleted: {event.src_path}")

    def on_modified(self, event):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{now}---Modified: {event.src_path}")

    def on_moved(self, event):
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        print(f"{now}---Moved: {event.src_path} to {event.dest_path}")


class FolderObserver:
    def __init__(self):
        self.observer = Observer()
        self.path = r'./../data'

    def launch(self):
        event_handler = Handler(patterns, ignore_patterns, ignore_directories, case_sensitive)
        go_recursively = True
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=go_recursively)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Stop Observation")
        self.observer.join()
