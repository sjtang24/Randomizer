import Experiment as ex
import Randomizer as r
from psychopy import core

# EXPERIMENT INFO: constants, etc.
NAME = "Perceptual Balance Task"
STIMULI_FILE = "behavioral_stimuli.csv"

## CHANGE THIS VALUE ###################################################
DEBUG = False
# debug should be False when you are actually running the experiment
########################################################################

def terminate(abrupt=False):
    """General quitting procedure"""
    exp.end_experiment(abrupt=abrupt)
    core.quit()
    
def check_for_quit():
    """Quitting during the experiment"""
    if randizer.check_quit():
        terminate(abrupt=True)
        
def check_proceed():
    button = None
    if randizer.check_keyboard("right"):
        button = "right"
    elif randizer.check_keyboard("1"):
        button = "1"
    elif randizer.check_keyboard("2"):
        button = "2"
    elif randizer.check_keyboard("3"):
        button = "3"
    if not button:
        return (False, button)
    return (True, button)
    
# PROGRAM BEGINS HERE
exp = ex.Experiment(NAME, STIMULI_FILE, nrounds=1 if DEBUG else 6, DEBUG=DEBUG) 
randizer = r.Randomizer(NAME, exp, DEBUG=DEBUG)
if randizer.start_up() != None:
    terminate(abrupt=True)
while not exp.experiment_complete():
    check_for_quit()
    exp.next_round()
    if randizer.announce_nxt_round(exp.current_round()) == -1:
        terminate(abrupt=True)
    currStim = exp.next_stimulus() # -1st to 0th (1st stimuli)
    while not exp.round_complete():
        check_for_quit()
        currStim = exp.current_stimulus()
        randizer.draw_round(exp.current_trial_info(), currStim)
        (should_proceed, button) = check_proceed()
        if should_proceed:
            confirm = randizer.next_confirm(warning=button)
            if confirm == -1:
                terminate(abrupt=True)
            elif confirm == True:
                currentStim = exp.next_stimulus(button)
randizer.end()
terminate()
