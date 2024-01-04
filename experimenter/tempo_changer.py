"""Tests the audacity pipe.

Keep pipe_test.py short!!
You can make more complicated longer tests to test other functionality
or to generate screenshots etc in other scripts.

Make sure Audacity is running first and that mod-script-pipe is enabled
before running this script.

Requires Python 2.7 or later. Python 3 is strongly recommended.

"""

import os
import sys

if sys.platform == 'win32':
    print("pipe-test.py, running on windows")
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    print("pipe-test.py, running on linux or mac")
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

print("Write to  \"" + TONAME +"\"")
if not os.path.exists(TONAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("Read from \"" + FROMNAME +"\"")
if not os.path.exists(FROMNAME):
    print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("-- Both pipes exist.  Good.")

TOFILE = open(TONAME, 'w')
print("-- File to write to has been opened")
FROMFILE = open(FROMNAME, 'rt')
print("-- File to read from has now been opened too\r\n")


def send_command(command):
    """Send a single command."""
    print("Send: >>> \n"+command)
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    """Return the command response."""
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    """Send one command, and return the response."""
    send_command(command)
    response = get_response()
    print("Rcvd: <<< \n" + response)
    return response

PATH_IN = "C:/Users/giaco/Desktop/mpc_miniproject/perturbations"
PATH_OUT = "C:/Users/giaco/Desktop/mpc_miniproject/results"

def quick_test():


    for filename in os.listdir(PATH_IN):

        original_tempo = int(filename[0:3])
        print(original_tempo)

        new_tempos = []
        while True:
            print("new bpm for the song")
            choice = input()
            if len(choice) > 1:
                new_tempos.append(int(choice))
            else:
                break
        print(f"{filename} (at {original_tempo} bpm) will be changed to {new_tempos}")

        for nt in new_tempos:
            do_command(f"Import2: Filename={os.path.join(PATH_IN, filename)}")
            do_command("SelectAll")
            do_command(f'ChangeTempo: Percentage={(nt / original_tempo - 1) * 100} SBSMS=False')

            outfilename = f"{nt:02}{filename[3:]}"
            do_command(f'Export2: Filename={os.path.join(PATH_OUT, outfilename)} NumChannels=2')
            do_command("TrackClose")


    """Example list of commands.
    filename = "060_carol_of_the_bells.mp3"
    do_command(f"Import2: Filename={os.path.join(PATH_IN, filename)}")

    do_command("SelectAll")

    original_tempo = 60
    derived_tempo = 61
    do_command(f'ChangeTempo: Percentage={(1 - derived_tempo / original_tempo) * 100} SBSMS=False')

    filename = "061_carol_of_the_bells.mp3"
    do_command(f'Export2: Filename={os.path.join(PATH_OUT, filename)} NumChannels=2')

    do_command("TrackClose")"""

quick_test()