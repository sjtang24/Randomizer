"""
The Experiment module deals with all things having to do with experimental 
control, like keeping track of the rounds, object numbers, stimuli, and trials,
along with dealing with the data collections throughout each of the trials. 
"""
import ExperimentData as datafile
import Stimuli as stim
from psychopy import core
import random

# CONSTANTS
TRIAL_HEADER = "Round #{}/{}\nObject #{}/{}\n(Trial #{}/{})"
COL = ["Trial#", "Round#", "Object#", "ObjectName", "ObjectRatioColors", \
"ObjectOrientation", "StartTime","EndTime","Duration","PrecisionGraspViolation"]
SCORING=["Time before First Grasp", "First Grasp Lift Off","Object Placed Down (Time)",
"(First) Held For","First Grasp Location", "First Grasp Precision","Time before Second Grasp",
"Second Grasp Lift Off", "(Second) Object Placed Down","(Second) Held For",
"Second Grasp Location","Second Grasp Precision"]

# CLASS
class Experiment:
    """
    The Experiment class is the blueprint for Experiment objects, which are 
    used to control the experiment. It acts sort of like an iterator.
    """
    def __init__(self, name, stimuli_list, nrounds=6, DEBUG=False):
        """ Creates an Experiment object.
        :param name: name of the experiment
        :type name: string
        :param stimuli_list: name of the path of the file to list of stimuli
        :type stimuli_list: string 
        :param col: the column names of the data to be collected throughout the experiment.
        :type col: string list
        :param nrounds: number of rounds in the experiment
        :type nrounds: int 
        """
        # Universal Information
        stims = stim.Stimuli(stimuli_list) # list of list of NovelObject's
        self.output = datafile.ExperimentData(experiment_name=name, columns=COL+SCORING, DEBUG=DEBUG)
        self.stimuli = stims.get_stimuli()
        self.nstims = stims.num_stimuli()
        self.nrounds = nrounds
        self.univ_clock = core.Clock()
        
        # Attributes descibing the state of the experiment (round, trial, stimuli)
        self.currentRound = 0
        self.currentStims = None
        self.currentObjectNum = -1
        self.trialStart = 0
        self.trialEnd = 0
        self.grasp_violation = "None"
        
        self.start_timer()
        
    def start_timer(self):
        self.univ_clock.reset()
        
    def experiment_complete(self): 
        """Returns whether the EXPERIMENT is complete"""
        return self.currentRound >= self.nrounds 
        
    def round_complete(self):
        """Returns whether the ROUND is complete"""
        return self.currentObjectNum >= self.nstims
            
    def next_round(self):
        """Advances the experiment to the next round, resets the stimuli, and 
        shuffles them. Requires the round but not the experiment is complete
        before doing so."""
        self.currentRound += 1
        self.currentObjectNum = -1
        self.currentStims = self.stimuli[1 - self.currentRound % 2]
        random.shuffle(self.currentStims) 
        
    def current_round(self):
        """Return the current round number"""
        return self.currentRound
        
    def current_stimulus(self):
        """Returns the current stimulus for the trial"""
        if self.currentStims != None:
            return self.currentStims[self.currentObjectNum]
        
    def current_trial_info(self):
        """
        Returns information about the current trial, including the object number
        in the round, the round number, and the number of trials in a format
        that is will be intended to be displayed to the user of the program.
        """
        tnum = self.trial_number()
        tottrls = self.nrounds * self.nstims
        return TRIAL_HEADER.format(self.currentRound, self.nrounds, self.currentObjectNum + 1, self.nstims, tnum, tottrls)

    def trial_number(self):
        """Calculates the trial number of from the classes attributes"""
        return (self.currentRound - 1) * self.nstims + self.currentObjectNum + 1
        
    def get_nstimuli(self):
        """Returns the number of objects in a single round"""
        return self.nstims
        
    def next_stimulus(self, button='right'):
        """Advances the experiment to the next object, making sure to update
        the datasheet beforehand"""
        self.trialEnd = self.univ_clock.getTime()
        if button == '1':
            self.grasp_violation = "Grasp #1"
        elif button == '2':
            self.grasp_violation = "Grasp #2"
        elif button == '3':
            self.grasp_violation = "Both Grasps"
        else:
            self.grasp_violation = "NONE"
        if self.currentObjectNum >= 0:
            self.update_info()
        self.currentObjectNum += 1
        self.trialStart = self.univ_clock.getTime()
    
    def update_info(self):
        """Updates the experimental data output file with a new entry of data 
        for the current state of the experiment.
        """
        trial_num = self.trial_number()
        round_num = self.currentRound
        object_num = self.currentObjectNum + 1
        obj = self.current_stimulus()
        objname = obj.get_stimuli()
        objinfo = obj.get_object_info()
        objorient = obj.get_orientation()
        duration = self.trialEnd - self.trialStart
        info = [trial_num, round_num, object_num, objname, objinfo, objorient, \
        self.trialStart, self.trialEnd, duration, self.grasp_violation]
        scoring_data = [""] * len(SCORING)
        self.output.update(info + scoring_data)
        
    def end_experiment(self, abrupt=False):
        """Aborts or uploads the output file depending on whether the experiment
        end early. (Note: if the program crashes, a file will be uploaded)"""
        if abrupt:
            print("No file will be created!")
            self.output.abort()
            return
        else:
            print("A file has been created!")
            self.output.done()
            return
