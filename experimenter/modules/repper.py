import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from modules import ed
from modules import wait
from modules import end
from modules import keytracker as kt




def gotoRepper(window, frame, ed: ed.ExperimentData):
    
    frame.destroy()
    frame = tk.LabelFrame(window, text="Repper", padx=50, pady=50)

    def keypressed(arg):
        ed.repper_ts[ed.repper_count-1].append(datetime.now().timestamp())

    def keyreleased(arg):
        pass

    key_tracker = kt.KeyTracker()
    key_tracker.track('space', keypressed, keyreleased)
    frame.bind_all('<KeyPress>', key_tracker.report_key_press)
    frame.bind_all('<KeyRelease>', key_tracker.report_key_release)

    def endPerturbation():
        ed.stop_perturb()
        ed.save()
        if ed.repper_count < ed.max_repper:
            wait.gotoWait(window, frame, ed)
        else:
            end.gotoEnd(window, frame, ed)


    def startPerturbation():
        ed.play_perturb()
        frame.after(60 * 1000, endPerturbation) # DURATION PERTURB (60s)

    def endReprise():
        ed.stop_metronome()
        frame.after(5 * 1000, startPerturbation) # DURATION BETWEEN REPRISE AND PERTURB (5s)

    frame.after(30 * 1000, endReprise) # DURATION OF REPRISE (30s)
    frame.pack(padx=5, pady=5)

    instructionLabel = tk.Label(master=frame, text="Please tap along the metronome. When the metronome stops, continue tapping, while trying to maintain the same tempo.")
    instructionLabel.pack()
    
    ed.calc_perturbation_tempo()
    ed.start_metronome()




    
