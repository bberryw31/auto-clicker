import tkinter as tk
import threading
import pyautogui
import random
import time
from pynput import keyboard

class AutoClicker:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.click_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.running = False

    def click_loop(self):
        while self.running:
            pyautogui.click()
            cursor_jitter()  # Simulate subtle twitch
            interval = random.uniform(0.190, 0.255)
            time.sleep(interval)


def listen_keys(clicker, status_label):
    def on_press(key):
        try:
            if key.char == '[':
                clicker.start()
                status_label.config(text="Status: Running")
            elif key.char == ']':
                clicker.stop()
                status_label.config(text="Status: Paused")
        except AttributeError:
            pass  # Special keys like shift, etc.

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()


def cursor_jitter():
    if random.random() < 0.15:  # 15% chance to jitter per cycle
        x, y = pyautogui.position()
        dx = random.choice([-2, -1, 1, 2])
        dy = random.choice([-2, -1, 1, 2])

        pyautogui.moveTo(x + dx, y + dy, duration=random.uniform(0.01, 0.03))
        pyautogui.moveTo(x, y, duration=random.uniform(0.01, 0.03))


def main():
    clicker = AutoClicker()

    # GUI setup
    root = tk.Tk()
    root.title("AutoClicker")
    root.attributes("-topmost", True)
    root.geometry("220x100")
    root.resizable(False, False)

    tk.Label(root, text="Press [ to Start\nPress ] to Pause").pack(pady=10)
    status_label = tk.Label(root, text="Status: Paused", fg="blue")
    status_label.pack()

    # Start keyboard listener
    listen_keys(clicker, status_label)

    root.mainloop()

if __name__ == "__main__":
    main()
