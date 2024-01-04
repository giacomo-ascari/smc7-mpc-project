import tkinter as tk
from tkinter import messagebox

from modules import ed
from modules import ready

consentText = "This is a request for your consent to process your personal data. The purpose of the processing is understanding the resilience of SPR to external musical perturbations. \n \
You consent to the processing of the following data about you: first name, occupation, experimental data of finger tapping.\n \
I, Giacomo Ascari, is the data controller of your data. \n \
Your data will be stored securely, and I will solely use the data for the above purpose. \n \
You always have the right to change your consent. If you wish to change your consent later on, you can contact the data controller directly or by email at gascar23@student.aau.dk. \n \
The General Data Protection Regulation entitles you to obtain information that you shared by contacting the data controller directly or by email at gascar23@student.aau.dk."

dutyText = "How I process your data \n \
\n \
​​​​​The data controller \n \
Giacomo Ascari, Brondbyoster Boulevard 28, 3. 03, 2605 Brondby, DK \n \
\n \
The purpose of processing your data \n \
Education and research \n \
\n \
I process the following personal data: \n \
General personal data (see Article 6(1) (a)) \n \
(E.g. name, address, email, age, self-published data etc.) \n \
In particular, first name, occupation, experimental data of finger tapping. \n \
\n \
Store your data \n \
I will store your personal data for as long as necessary for the data processing purpose for which I are obtaining your consent and in accordance with the applicable legislation. I will then erase your personal data. \n \
\n \
Your rights \n \
When I process your personal data, you have several rights under the General Data Protection Regulation. For example, you have a right to erasure and a right to data portability. \n \
In certain cases, you have a right of access, a right to rectification, a right to restriction of processing and a right to object to our processing of the personal data in question. \n \
Be aware that you cannot withdraw your consent with retroactive effect. \n \
\n \
Do you want to complain? \n \
If you believe that I do not meet my responsibility or that I do not process your data according to the rules, you may lodge a complaint with the Danish Data Protection Agency at dt@datatilsynet.dk. \n \
However, I encourage you also to contact us, as I want to do me utmost to accommodate your complaint."

def gotoConsent(window, frame, ed: ed.ExperimentData):
    
    frame.destroy()
    frame = tk.LabelFrame(window, text="Consent", padx=50, pady=50)
    frame.pack(padx=5, pady=5)

    consent = tk.IntVar()

    consentLabel = tk.Label(master=frame, text=consentText)

    def onConsentButton():
        ed.consent = True
        ed.consent_ts = ed.get_ts()
        ed.save()
        ready.gotoReady(window, frame, ed)
        
    consentButton = tk.Button(
        master=frame,
        text="Continue",
        state='disabled',
        command=onConsentButton
    )

    def onConsentCheck():
        if consent.get():
            consentButton['state'] = 'normal'
        else:
            consentButton['state'] = 'disabled'

    consentCheck = tk.Checkbutton(
        master=frame,
        text="I hereby consent to Giacomo Ascari processing my data in accordance with the above purpose and information.",
        variable=consent,
        command=onConsentCheck
    )

    def dutyMessage():
        messagebox.showinfo(title="Duty to inform: how I process your data", message=dutyText)


    consentDutyButton = tk.Button(
        master=frame,
        text="Duty to inform: how I process your data",
        command=dutyMessage
    )        

    consentLabel.pack()
    consentCheck.pack()
    consentButton.pack()
    consentDutyButton.pack()
