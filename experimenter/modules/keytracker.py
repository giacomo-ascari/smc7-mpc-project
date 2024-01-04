import threading
from datetime import datetime

class KeyTracker():
    key = ''    
    last_press_time = 0
    last_release_time = 0

    def track(self, key, on_key_press, on_key_release):
        self.key = key
        self.on_key_press = on_key_press
        self.on_key_release = on_key_release

    def is_pressed(self):
        return datetime.now().timestamp()   - self.last_press_time < .1

    def report_key_press(self, event):
        if event.keysym == self.key:
            if not self.is_pressed():
                self.on_key_press(event)
            self.last_press_time = datetime.now().timestamp()  

    def report_key_release(self, event):
        if event.keysym == self.key:
            timer = threading.Timer(.1, self.report_key_release_callback, args=[event])
            timer.start()

    def report_key_release_callback(self, event):
        if not self.is_pressed():
            self.on_key_release(event)
        self.last_release_time = datetime.now().timestamp()  