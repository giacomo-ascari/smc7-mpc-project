import tkinter as tk

from modules import ed

def gotoEnd(window, frame, ed: ed.ExperimentData):
    
    frame.destroy()
    frame = tk.LabelFrame(window, text="Conclusion", padx=50, pady=50)
    frame.pack(padx=5, pady=5)

    endLabel = tk.Label(master=frame, text="The experiment has finished. Thank you for your participation")
    endLabel.pack()

