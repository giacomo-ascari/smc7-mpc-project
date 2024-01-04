import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from modules import ed
from modules import wait
from modules import keytracker as kt

def gotoBaseline(window, frame, ed: ed.ExperimentData):

    frame.destroy()
    frame = tk.LabelFrame(window, text="Baseline SPR collection", padx=50, pady=50)

    def baselineEstablished():
        ed.calc_baseline_tempo()
        ed.save()
        wait.gotoWait(window, frame, ed)

    def keypressed(arg):
        if len(ed.baseline_ts) == 0:
            frame.after(30 * 1000, baselineEstablished) # DURATION OF BASELINE COLLECTION (30s)
        ed.baseline_ts.append(datetime.now().timestamp())

    def keyreleased(arg):
        pass

    key_tracker = kt.KeyTracker()
    key_tracker.track('space', keypressed, keyreleased)
    frame.bind_all('<KeyPress>', key_tracker.report_key_press)
    frame.bind_all('<KeyRelease>', key_tracker.report_key_release)
    frame.pack(padx=5, pady=5)

    instructionLabel = tk.Label(master=frame, text="Please begin tapping the spacebar at regular intervals at your preferred tempo. You may start when you feel ready.")
    instructionLabel.pack()
    
