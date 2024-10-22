import sys
import time
import itertools
import threading

class SpinningCursor:
    def __init__(self, delay=0.1, cursor_chars='|/-\\'):
        self.spinner_cycle = itertools.cycle(cursor_chars)
        self.delay = delay
        self.busy = False
        self.spinner_visible = False

    def write_next(self):
        while self.busy:
            if self.spinner_visible:
                sys.stdout.write('\b')
            char = next(self.spinner_cycle)
            sys.stdout.write(char)
            self.spinner_visible = True
            sys.stdout.flush()
            time.sleep(self.delay)

    def __enter__(self):
        self.busy = True
        self.thread = threading.Thread(target=self.write_next)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.busy = False
        time.sleep(self.delay)
        if self.spinner_visible:
            sys.stdout.write('\b')
            sys.stdout.flush()

if __name__ == '__main__':
    print('Loading data...', end='')
    with SpinningCursor():

        time.sleep(5)
    print('Done!')

    print('\nProcessing with custom spinner...', end='')
    with SpinningCursor(delay=0.2, cursor_chars='🌑🌒🌓🌔🌕🌖🌗🌘'):

        time.sleep(5)
    print('Done!')
