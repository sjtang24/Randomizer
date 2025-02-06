"""
ExperimentData.py is a module used to make file concerning the data collected
during the run of the Randomizer. 

It prompts the user for information, which is uses the name the file. Throughout 
the program, data may be added to the file, and such file can be closed.
"""

from psychopy import gui, data, core
import os

# The following functions are used to ensure valid input, particularly the 
# date. We want the number of days to match of with the month.
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def isLeapYear(yr):
    """Determines if the current year is a leap year.
    :param yr: the year
    :type yr: int 
    :rtype: bool
    :return: if the current year is a leap year
    """
    return yr % 4 == 0 and (not yr % 100 == 0 or yr % 400 == 0)

def getValidNumDays(month, year):
    """Gets the maximum number of days in a month
    :param month: the month
    :type: string 
    :param year: the year
    :type: int 
    :rtype: int
    :return stims: maximum number of days in the month of the given year; or
    -1 if the month is not valid.
    """
    if month in ["JAN","MAR","MAY","JUL","AUG","OCT","DEC"]:
        return 31
    elif month in ["APR", "JUN", "SEP", "NOV"]:
        return 30
    elif month in ["FEB"]:
        days = 28
        if isLeapYear(int(year)):
            days += 1
        return days
    return -1

def initializeFile(expname, dID = "", dS = 0, dY = 2022, dM = "", dD = 0, dScorer=-1, review=False):
    """Returns the name of the output file depending on the responses that the
    user gives when they begin the experiment. 
    :param expname: name of the experiment
    :type expname: string
    :param dID: participant id
    :type dID: string
    :param dS: session id
    :type dS: int 
    :param dY: year
    :type dY: int
    :param dM: month
    :type dM: string 
    :param dD: day    
    :type dD: int
    :rtype: string 
    :return: the name of the file for the current experimental session
    """
    name = "".join(expname.split(" "))
    # continue until the responses become valid
    filename = ""
    while review or (not review and not (dID and dY and dM and dD and dScorer \
        and 1 <= dD <= getValidNumDays(dM, dD) and dScorer > 0)):
        # updates the dialog
        exp_info = gui.Dlg(title=expname)
        exp_info.addText("---PARTICIPANT INFO---")
        exp_info.addField("Participant ID: ", dID)
        exp_info.addField("Session ID: ", initial=dS, choices=["BehavioralTraining","MRI-Part 1","MRI-Part 2"])
        exp_info.addText("---DATE INFO---")
        exp_info.addField("Year:", dY)
        exp_info.addField("Month:", choices=MONTHS, initial=dM)
        exp_info.addField("Day: ", dD)
        exp_info.addText("---SCORING INFO---")
        exp_info.addField("Number of people scoring the data:", initial=3)
        results = exp_info.show()
        if exp_info.OK:
            # user presses ok
            try:
                dID = results[0]
                dS = results[1]
                dY = int(results[2])
                dM = results[3]
                dD = int(results[4])
                dScorer = int(results[5])
                review = False
            except ValueError:
                pass
        else:
            # user cancels
            print("Cancelled!")
            return None
    # returns the name of the file        
    names = []
    scoring_info = gui.Dlg(title="Scoring Menu")
    for i in range(dScorer):
        default = ""
        if i == 0:
            default = "Marty"
        elif i == 1:
            default = "Tijana"
        elif i == 2:
            default = "Steven"
        else: 
            default = "Scorer #" + str(i + 1)
        scoring_info.addField("Scorer #" + str(i + 1), default)
    filename = "{}-PID{}-{}_{}{}{}".format(name, dID, dS, dY, dM, dD)
    names = scoring_info.show()
    if scoring_info.OK:
        return (filename, dScorer, names)
    else:
        return initializeFile(expname, dID, dS, dY, dM, dD, dScorer, review=True)
    
class ExperimentData: 
    """
    This class defines an ExperimentData object. It makes a file that the client
    can update and close. 
    """
    def __init__(self, experiment_name="", columns=[], DEBUG=False):
        """
        Construct an instance of an ExperimentData object.
        :param experiment_name: name of the experiment to name the file
        :type experiment_name: string
        :param columns: the name of the column of data expected to be added into the file.
        :type columns: string list 
        """
        init = initializeFile(experiment_name)
        if init:
            (filename, dScorer, names) = init
            if not filename:
                core.quit()
        else:
            core.quit()
        folder = "data" if not DEBUG else "tests"
        filepath = os.getcwd() + os.sep + folder + os.sep + filename
        self.columns = columns
        self.experiment_name = experiment_name
        self.d = data.ExperimentHandler(name=self.experiment_name, dataFileName=filepath)
        self.numScorers = dScorer
        self.namesScorers = names

    def update(self, vals=[]):
        """
        Updates the output file with a row (array) of data. Entries should be None
        if such data is unavailable. 
        :param vals: array of new data
        :type vals: list
        """
        it = 0
        while it < self.numScorers:
            nvals = len(vals)
            ncols = len(self.columns)
            self.d.addData("Scorer Name", self.namesScorers[it])
            for i in range(0, nvals):
                self.d.addData(self.columns[i], vals[i])
                
            self.d.nextEntry()
            it += 1
        
    def done(self):
        """Closes the file"""
        self.d.close()
        
    def abort(self):
        self.d.abort()
