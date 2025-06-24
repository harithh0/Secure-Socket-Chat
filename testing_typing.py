import threading
import time

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout

session = PromptSession()


def background_messages():
    # Simulate incoming messages
    while True:
        time.sleep(3)
        with patch_stdout():
            print("\n[Friend]: Hello!")


def main():
    threading.Thread(target=background_messages, daemon=True).start()
    while True:
        user_input = session.prompt("> ")
        print(f"You: {user_input}")


main()
