import tkinter as tk
from tkinter import messagebox

from modules import ed
from modules import repper

def gotoWait(window, frame, ed: ed.ExperimentData):
    
    frame.destroy()
    frame = tk.LabelFrame(window, text=f"Test {ed.repper_count+1}/{ed.max_repper}", padx=50, pady=50)
    frame.pack(padx=5, pady=5)

    ready = tk.IntVar()

    def onStartButton():
        ed.save()
        repper.gotoRepper(window, frame, ed)

    startButton = tk.Button(
        master=frame,
        text="Start",
        state="disabled",
        command=onStartButton
    )

    def onReadyCheck():
        if ready.get():
            startButton['state'] = 'normal'
        else:
            startButton['state'] = 'disabled'

    readyCheck = tk.Checkbutton(
        master=frame,
        text="I received instructions about the experiment and I'm ready to start",
        variable=ready,
        command=onReadyCheck
    )

    readyCheck.pack()
    startButton.pack()

    
