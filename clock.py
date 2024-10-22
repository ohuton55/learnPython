import tkinter as tk
import time
import signal
import sys
import itertools
import threading

class SpinningWidget(tk.Label):
    def __init__(self, parent, cursor_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏', delay=0.1):
        super().__init__(
            parent,
            font=('calibri', 15),
            background='black',
            foreground='white'
        )
        self.cursor_chars = cursor_chars
        self.delay = delay
        self.spinning = False
        self.cursor_cycle = itertools.cycle(self.cursor_chars)

    def start(self):
        self.spinning = True
        self.spin_thread = threading.Thread(target=self._spin)
        self.spin_thread.daemon = True
        self.spin_thread.start()

    def stop(self):
        self.spinning = False

    def _spin(self):
        while self.spinning:
            char = next(self.cursor_cycle)
            self.after(0, self.config, {'text': char})
            time.sleep(self.delay)

class Clock(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Always-On Clock")
        self.attributes('-topmost', True) # Keep window on top
        self.overrideredirect(True) # Remove window decorations

        # Create a frame to hold both widgets
        self.frame = tk.Frame(self, background='black')
        self.frame.pack(padx=0, pady=0)

        # Spinner widget
        self.spinner_left = SpinningWidget(self.frame, '🌑🌒🌓🌔🌕🌖🌗🌘', 1.5)
        self.spinner_left.pack(side='left', padx=5)

        self.spinner_right = SpinningWidget(self.frame)
        self.spinner_right.pack(side='right', padx=5)

        # Clock Label
        self.label = tk.Label(
            self.frame,
            font=('calibri', 20, 'bold'),
            background='black',
            foreground='white'
        )
        self.label.pack(side='top', anchor='center')

        self.geometry("+1600+0")   # Adjust these values to position 
        self.label.bind("<Button-1>", self.close_app)   # Bind left-click

        self.update_time()
        self.spinner_left.start()
        self.spinner_right.start()

    def update_time(self):
        current_time = time.strftime('%H:%M:%S')
        self.label.config(text=current_time)
        self.after(1000, self.update_time)  # Update every second

    def close_app(self, event=None):
        self.spinner_left.stop()
        self.spinner_right.stop()
        self.quit()

def signal_handler(signal, frame):
    print("\nProgram exiting gracefully.")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    clock = Clock()
    clock.mainloop()


