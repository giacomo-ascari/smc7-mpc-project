import math
import os
from datetime import datetime
from playsound import playsound
import threading
import time
import random
import string

import vlc

def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

class ExperimentData:

    def __init__(self):
        self.folder = os.path.join("data", random_string_generator(10, string.digits + string.ascii_lowercase))
        self.stop_it = False
        self.thread = None
        self.max_repper = 4
        #                    16,   -8,   -4,   0,   +4,   +8,  +16  %
        self.deviations = [0.84, 0.92, 0.96, 1.0, 1.04, 1.08, 1.16]
        self.media = None
        # \\ GENERAL DATA //
        self.name = ""
        self.musician = False
        self.consent = False
        self.consent_ts = 0
        self.experimenter_ts = 0
        # \\ EXP DATA //
        self.baseline_ts = []
        self.repper_count = 0
        self.repper_ts = []
        # \\ PROC DATA //
        self.baseline_tempo = 0
        self.perturbation_tempo = []
        pass

    def get_ts(self):
        return datetime.now().timestamp()
    
    def start_metronome(self):
        def thread_function():
            
            interval = 60 / self.baseline_tempo
            start = self.get_ts()
            media: vlc.MediaPlayer = vlc.MediaPlayer("cowbell_sample.mp3")

            while not self.stop_it:
                if self.get_ts() > start + interval:
                    #print(self.get_ts() - start)
                    start = self.get_ts()
                    media.play()
                    media: vlc.MediaPlayer = vlc.MediaPlayer("cowbell_sample.mp3")

                    
        self.thread = threading.Thread(target=thread_function)
        self.thread.start()
        print("metronome started")

    def stop_metronome(self):
        if self.thread != None:
            self.stop_it = True
            self.thread.join()
            self.stop_it = False
            print("metronome stopped")

    def play_perturb(self):
        files = os.listdir("perturbations")
        filename = "cowbell_sample.mp3"
        for f in files:
            if int(f[:3]) == math.floor(self.perturbation_tempo[self.repper_count-1]):
                filename = os.path.join("perturbations", f)
                self.media: vlc.MediaPlayer = vlc.MediaPlayer(filename)
                self.media.play()
                print(filename)
                break
    
    def stop_perturb(self):
        if self.media != None:
            self.media.stop()
        

    def save(self):

        if not os.path.exists(self.folder):
            os.mkdir(self.folder)

        with open(os.path.join(self.folder, "general_data.txt"), 'w') as f:
            f.write("name " + str(self.name) + "\n")
            f.write("musician " + str(self.musician) + "\n")
            f.write("consent " + str(self.consent) + "\n")
            f.write("consent_ts " + str(self.consent_ts) + "\n")
            f.write("experimenter_ts " + str(self.experimenter_ts) + "\n")

        with open(os.path.join(self.folder, "baseline_ts.txt"), 'w') as f:
            for ts in self.baseline_ts:
                f.write(str(ts) + "\n")
        for i in range(self.repper_count):
            with open(os.path.join(self.folder, f"repper_ts_{i}.txt"), 'w') as f:
                for ts in self.repper_ts[i]:
                    f.write(str(ts) + "\n")
        
        with open(os.path.join(self.folder, "proc_data.txt"), 'w') as f:
            f.write("baseline_tempo " + str(self.baseline_tempo) + "\n")
            for pt in self.perturbation_tempo:
                f.write("pt " + str(pt) + "\n")

    def calc_perturbation_tempo(self):
        # +-4, +-8, +-16
        self.repper_count += 1
        self.repper_ts.append([])
        
        attempt = 0
        valid = False
        while not valid:

            index = random.randint(0, len(self.deviations)-1)
            attempt = self.baseline_tempo * self.deviations[index]
            if attempt <= 190 and attempt >= 60:
                valid = True
                del self.deviations[index]
        
        self.perturbation_tempo.append(attempt)
        print("pt", self.perturbation_tempo)

    def calc_baseline_tempo(self):

        ioi = []
        for i in range(1, len(self.baseline_ts)):
            ioi.append(self.baseline_ts[i] - self.baseline_ts[i-1])
        
        avg5 = []
        for i in range(4, len(ioi)):
            v = ioi[i-4] + ioi[i-3] + ioi[i-2] + ioi[i-1] + ioi[i]
            avg5.append(v / 5)
        
        bpm = []
        for i in range(0, len(avg5)):
            bpm.append(1 / avg5[i] * 60)
        
        avg2ndhalf = 0
        count = 0
        for i in range(math.floor(len(bpm)/2), len(bpm)):
            avg2ndhalf += bpm[i]
            count += 1
        if count > 0:
            avg2ndhalf /= count

        if avg2ndhalf > 190:
            self.baseline_tempo = 190
        elif avg2ndhalf < 60:
            self.baseline_tempo = 60
        else:
            self.baseline_tempo = avg2ndhalf
        print(avg2ndhalf, self.baseline_tempo)