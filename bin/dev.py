from collections.abc import Callable
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import re
import threading
import time
from typing import Any
from watchdog.observers import Observer
from watchdog.events import (
    PatternMatchingEventHandler,
)
from build import build, BUILD_ROOT, PROJECT_ROOT


class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BUILD_ROOT, **kwargs)


class DevServer:
    def __init__(self):
        self.httpd = HTTPServer(("", 8000), RequestHandler)
        self.reload_event = threading.Event()
        self.stop_event = threading.Event()

    def _serve(self):
        print("Starting server...")
        server_thread = threading.Thread(target=self.httpd.serve_forever)
        server_thread.start()
        print("Server running on http://localhost:8000")

        self.reload_event.wait()
        if self.stop_event.is_set():
            print("Stopping server...")
        else:
            print("Reloading server...")

        self.httpd.shutdown()
        server_thread.join()

        self.reload_event.clear()

        if not self.stop_event.is_set():
            self._serve()

    def serve(self):
        threading.Thread(target=self._serve).start()

    def reload(self):
        self.reload_event.set()

    def stop(self):
        self.stop_event.set()
        self.reload_event.set()


class Debouncer:
    def __init__(self, delay=0.5):
        self.delay = delay
        self.timer = None

    def debounce(self, func: Callable[..., None]) -> Callable[..., None]:
        def wrapper(*args, **kwargs):
            if self.timer:
                self.timer.cancel()
            self.timer = threading.Timer(self.delay, func, args, kwargs)
            self.timer.start()

        return wrapper


class DevEventHandler(PatternMatchingEventHandler):
    def __init__(self, server, *args, **kwargs):
        super().__init__(
            *args,
            patterns=["*.html", "*.css", ".svg"],
            **kwargs,
        )
        self.server = server

    def on_modified(self, event):
        super().on_modified(event)
        self._on_modified(event)

    def __on_modified(self, event):
        if not re.match(r".*build.*", event.src_path):
            print(f"File {event.src_path} has been modified")
            build()
            self.server.reload()

    _on_modified = Debouncer().debounce(__on_modified)


def watch():
    server = DevServer()
    server.serve()

    observer = Observer()
    event_handler = DevEventHandler(server)

    observer.schedule(event_handler, path=PROJECT_ROOT, recursive=True)
    observer.start()

    print("Watching for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        server.stop()

    observer.join()


if __name__ == "__main__":
    build()
    watch()
