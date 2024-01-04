import tkinter as tk
from tkinter import messagebox
from modules import ed
from modules import baseline

def gotoReady(window, frame, ed: ed.ExperimentData):
    
    musician = tk.IntVar()
    name = tk.StringVar()
    ready = tk.IntVar()

    frame.destroy()
    frame = tk.LabelFrame(window, text="Preparation", padx=50, pady=50)
    frame.pack(padx=5, pady=5)

    nameLabel = tk.Label(master=frame, text="Please write down your first name. This will serve as the identifier of the experiment")
    nameEntry = tk.Entry(master=frame, textvariable=name)

    def onStartButton():
        ed.name = name.get()
        ed.musician = musician.get()
        ed.save()
        baseline.gotoBaseline(window, frame, ed)

    startButton = tk.Button(
        master=frame,
        text="Start",
        state="disabled",
        command=onStartButton
    )

    musicianLabel = tk.Label(master=frame, text="For the scope of the experiment, a participant is a musician if at least one of the following two conditions is true: \n \
                             - they received musical training privately \n\
                             - they studied an instrument and/or performed for at least two years \n ")
    musicianCheck = tk.Checkbutton(
        master=frame,
        text="I consider myself a musician",
        variable=musician,
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
    

    nameLabel.pack()
    nameEntry.pack()
    musicianLabel.pack()
    musicianCheck.pack()
    readyCheck.pack()
    startButton.pack()
    
