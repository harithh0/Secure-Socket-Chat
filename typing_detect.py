import threading
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings


class TypingTracker:

    def __init__(self, timeout=2.0):
        self.typing = False
        self.last_key_time = time.time()
        self.timeout = timeout

    def register_keypress(self):
        self.last_key_time = time.time()
        if not self.typing:
            self.typing = True
            print("[Typing started]")

    def monitor(self):
        while True:
            if self.typing and time.time() - self.last_key_time > self.timeout:
                self.typing = False
                print("[Typing stopped]")
            time.sleep(0.1)


typing_tracker = TypingTracker(timeout=2.0)

kb = KeyBindings()


# addds a wildcard key binding (basic characters, backspace, etc.)
@kb.add("<any>")
def handle_any(event):
    typing_tracker.register_keypress()


session = PromptSession(key_bindings=kb)

threading.Thread(target=typing_tracker.monitor, daemon=True).start()

while True:
    text = session.prompt("> ")
    print(f"You said: {text}")
