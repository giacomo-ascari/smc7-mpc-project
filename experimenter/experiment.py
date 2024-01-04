# FOR GRAPHICAL INTERFACE
import tkinter as tk


# STATES:  CONSENT, READY, WAIT, BASELINE, REPRISAL, PERTURB
from modules import consent
from modules import ed

# EXPERIMENTAL DATA
ed = ed.ExperimentData()
ed.experimenter_ts = ed.get_ts()

# GRAPHICAL INTERFACE
window = tk.Tk(className=ed.folder)
window.geometry("1200x600")
frame = tk.LabelFrame(window)

def main():

    # GOTO TO CONSENT FRAME
    consent.gotoConsent(window, frame, ed)
    
    # EVEN LOOP, NO TOUCHY
    window.mainloop()

if __name__ == "__main__":
    main()
