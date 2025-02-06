"""
The Randomizer Modules does a bulk of the tasks with regards to the Graphical
Interface and user interactions with the program. 
"""
from psychopy.visual import window
from psychopy import visual, core
from psychopy.hardware import keyboard 
import NovelObject

# Constants, Textual Information, and Templates
SECONDS_BETW_TRIAL = 3
REVERT_MESSAGE = """Are you sure you are done with this object?\n\n\n\n\n\n\n\n\n\n\n\n[Click 'return' to revert in {} seconds]"""
WELCOME_MESSAGE ="""THIS PROGRAM IS COMPLEMENTARY TO THE TRAINING OF EMEFA'S "PERCEPTUAL BALANCE BEHAVIORAL RESEARCH STUDY"

Directions:
    1) At any time while running the program, you can quit by clicking <esc>. It'll take you to an exit message for a couple seconds before actually terminating. A timer will start when you click the spacebar. 
    2) For each stimulus, you will see the image of the object, the ratios of each color, and information about the current trial.
    3) The image shown is from the experimenter's perspective. When the object is placed down, the color on the left as shown in the screen should appear on your left, and vice versa. This means that the measuring tape is visible.
    4) You are "done" with the object when you place the object back in the box. When you do so, rotate the object such that the color on the left appears on the right and vice versa.
    5) During each trial, you should observe the participant, and make sure they use a precision grasp. If they fail to use such a grasp only on the first grasp, click "1"; if they do so only on the second grasp, click "2"; if they do so on both, click "3"; if they successfully use the precision grasp, proceed normally to #6. A screen will pop up confirming your indications. 
        a) If this is intentional, notify the participant and correct their grasp. Click <right> to proceed through the experiment. Once you do so, the program will indicate that the CSV file will be marked accordingly and then proceed to the next object. You won't be allowed to proceed back to the object after.
        b) If this is not intentional, click <return> key to revert back to the object. 
    6) Once you are done with a stimulus, click the <right> arrow key. 
        a) If this is intentional, wait 3 seconds. Note you will not be able to come back to it. If everything goes normally, "None" will be recorded in the CSV file.
        b) If this is not intentional, you have 3 seconds to click the <return> key to revert back to the previous stimulus.
    7) The experiment will end after 6 rounds of 9 objects (54 trials in total).
    8) If there are no interruptions in the experiment, a timelog giving the list of all of the objects will be downloaded to the 'data' folder or 'tests' folder (if in DEBUG mode). If you quit the program, there will not be output. The only exception is if the program crashes in which an output file will be uploaded. If during experimentation the program crashes, please let me know as soon as possible. 
    9) Between rounds, you can click 'i' to review these instructions again, but for more information, you can take a look at the Randomizer instructions.

CLICK <SPACEBAR> TO CONTINUE
"""
CONCLUDING_MESSAGE = "The experiment has finished...\n\nYou have given the participant all of the stimuli!\n\n"
DISPLAY_ROUND_MESSAGE = "ROUND {}\n\n[Click the <RIGHT ARROW> to continue or <i> to review the instructions]"
CONFIRM_NEXT_ROUND = "The next round is starting in {} seconds...\n [Click <return> to revert]"
GRASP_WARNING = "You have indicated that the user didn't use the precision grasp on {}!\n\n\n\n\n\n\n\n\n\n\n\n\nTake a moment to correct the participant's grasp.\n[Click 'return' to revert OR 'right' to continue]"
CONFIRM_WARNING = "We'll mark in the CSV that the participant did not use the precision grasp on {}!"

class Randomizer:
    """
    The Randomizer class does creates an instance of a Randomizer object, used
    for the graphical interface of the Randomizer.
    """
    def __init__(self, name, snds=SECONDS_BETW_TRIAL, DEBUG=False):
        """Constructs a Randomizer object as described.
        """
        SECONDS_BETW_TRIAL = snds
        self.experimenter_window = window.Window(fullscr = not DEBUG, color = "#2f3fa8")
        self.main_kb = keyboard.Keyboard()
        self.main_timer = core.Clock()
        self.intro_screen = visual.TextStim(self.experimenter_window, text=WELCOME_MESSAGE, height=0.05, wrapWidth = 1.75, alignText="left")
        self.concluding_screen = visual.TextStim(self.experimenter_window, text=CONCLUDING_MESSAGE)
        self.round_info = visual.TextStim(self.experimenter_window, wrapWidth = 1.5, color="white", bold=True, height=0.1, pos=(0,0.75))
        self.next_round = visual.TextStim(self.experimenter_window, wrapWidth = 1.5, height=0.1)
        self.next_round_confirm = visual.TextStim(self.experimenter_window, wrapWidth = 1.5, height=0.1)
        self.confirm_warning = visual.TextStim(self.experimenter_window, wrapWidth = 1.5, height=0.1)
        self.lhs_label = visual.TextStim(self.experimenter_window, pos = (-0.25,-0.6))
        self.rhs_label = visual.TextStim(self.experimenter_window, pos = (0.25,-0.6))
        self.uniform_label = visual.TextStim(self.experimenter_window, pos = (0, -0.6))
        self.image_stim = visual.ImageStim(self.experimenter_window, size=[1, 1])
    
    def display_message(self, text_stim, time=SECONDS_BETW_TRIAL, end=False):
        """ Displays a given message for as long as need.
        :param text_stim: the message to be displayed
        :time: the amount of time in second to show the message
        :end: whether or not anytime during the message, the randomizer should 
        check if the program has ended or not (and avoid an infinite loop
        """
        self.main_timer.reset()
        while self.main_timer.getTime() < time: 
            if not end and self.check_quit():
                return -1
            text_stim.draw() 
            self.experimenter_window.flip()
  
    def check_quit(self):
        """
        Checks if the experiment has ended. If so, it executes the termination
        process, informing the user that the experiment has ended early. 
        """
        if "escape" in self.main_kb.getKeys(clear=False):
            self.concluding_screen.setText("THE EXPERIMENT HAS FINISHED EARLY!")
            self.end()
            return True
        return False
            
    def end(self, time = 3):
        """
        Generalized termination conditions regardless of whether the quit was
        abrupt or not. Ensures that last message cannot be "re-quittable."
        :param time: the amount of time to spend on the concluding screen.
        :type time: int 
        """
        self.display_message(self.concluding_screen, time=time, end=True)
        self.experimenter_window.close() 
            
    def start_up(self):
        """Starts of the experiment, showing the instruction of the randomizer,
        again giving the user the opportunity to quit when need, and space to
        continue using it.
        """
        self.main_kb.clearEvents()
        while "space" not in self.main_kb.getKeys(clear=False):
            if self.check_quit():
                return -1
            self.intro_screen.draw()
            self.experimenter_window.flip()

    def announce_nxt_round(self, roundnum, time=3):
        """
        Announces the next round of the experiment, giving the user the
        opportunity to quit when need.
        :returns None: if everything goes okay
        :returns -1: if the user decides to quit
        """
        dispMess = DISPLAY_ROUND_MESSAGE.format(roundnum)
        self.next_round.setText(dispMess)
        self.main_kb.clearEvents()
        while "right" not in self.main_kb.getKeys(clear=False):
            if self.check_keyboard("i"):
                self.start_up()
                self.main_kb.clearEvents()
            if self.check_quit():
                return -1
            self.next_round.draw()
            self.experimenter_window.flip()
        self.main_timer.reset()
        curr = self.main_timer.getTime()
        self.main_kb.clearEvents()
        while curr < time:
            if self.check_quit():
                return -1
            if "return" in self.main_kb.getKeys():
                self.announce_nxt_round(roundnum)
                break
            timeLeft = int(time - curr + 1)
            confirmNext = CONFIRM_NEXT_ROUND.format(timeLeft)
            self.next_round_confirm.setText(confirmNext)
            self.next_round_confirm.draw()
            self.experimenter_window.flip()
            curr = self.main_timer.getTime()
        self.main_kb.clearEvents()
      
    def check_keyboard(self, key):
        """Determines if the given key is pressed.
        :param key: the key to look out for
        """
        pressed = key in self.main_kb.getKeys(clear=False)
        if pressed:
            self.main_kb.clearEvents()
        return pressed
        
    def make_labels(self, stim):
        """
        Updates the necessary label type with the correct color and label
        depending on the stimuli given as input.
        :param stim: the current stimulus
        :type stim: NovelObject
        :rtype labels: visual.TextStim list
        :return labels: Text Stimuli holding the labels of the stimulus.
        """
        labels = stim.get_labels()
        labelStim = []
        if stim.is_uniform_object():
            (name, color) = labels[0]
            self.uniform_label.setText(name)
            self.uniform_label.setColor(NovelObject.get_display_color(color))
            labelStim.append(self.uniform_label)
        else:
            ((llabel, c1), (rlabel, c2)) = (labels[0], labels[1])
            self.lhs_label.setText(llabel)
            self.rhs_label.setText(rlabel)
            self.lhs_label.setColor(NovelObject.get_display_color(c1))
            self.rhs_label.setColor(NovelObject.get_display_color(c2))
            labelStim.append(self.lhs_label)
            labelStim.append(self.rhs_label)
        return labelStim
        
    
    def next_confirm(self, warning='right'):
        """
        Allows the user to confirm that they finished using the object, and 
        gives them the opportunity to quit if needed. It also handles the cases
        when a precision grasp is not used. 
        :returns: -1 if experiment is over, True if the experiment should move on, 
        and False if the experiment should continue using the same stimulus
        """
        self.main_timer.reset()
        grasp = ""
        while (warning == 'right' and self.main_timer.getTime() < SECONDS_BETW_TRIAL) or\
            (warning != 'right' and not self.check_keyboard("right")):
            if self.check_quit():
                return -1
            message = ""
            if warning == "1":
                grasp = "THE FIRST GRASP"
            elif warning == "2":
                grasp = "THE SECOND GRASP"
            elif warning == "3":
                grasp = "BOTH GRASPS"
            if "return" in self.main_kb.getKeys(clear=False):
                self.main_kb.clearEvents()
                return False
            if warning == 'right':
                message = REVERT_MESSAGE.format(SECONDS_BETW_TRIAL - int(self.main_timer.getTime()))
            else:
                message = GRASP_WARNING.format(grasp)
                self.next_round.setColor("yellow")
            self.next_round.setText(message)
            self.image_stim.draw()
            self.next_round.draw() 
            self.experimenter_window.flip()
            self.next_round.setColor("white")
        self.main_kb.clearEvents()
        if warning != "right":
            self.confirm_warning.setText(CONFIRM_WARNING.format(grasp))
            self.display_message(self.confirm_warning)
        self.main_kb.clearEvents()
        return True
       
    def draw_round(self, info, stim):
        """Updates the screen with the current stimulus and information.
        :param info: the trial information (round number, object number, and trial number)
        :type info: string
        :param stim: the stimulus 
        :type stim: NovelObject
        """
        self.round_info.text = info
        self.image_stim.setImage(stim.get_stimuli())
        self.round_info.draw()
        self.image_stim.draw()
        for lab in self.make_labels(stim):
            lab.draw()
        self.experimenter_window.flip()
        
