"""
Stimuli.py is a module used to describe lists of NovelObjects, with several helper
functions used by the class held in the module. 

It essentially creates "Stimuli" to prepare for the experiment. To do so, it takes
a list of viable stimuli, sorts them into uniform objects, flipped nonuniform objects,
and unflipped nonuniform objects. Then, it ensures that sets of stimuli used will 
contain all the uniform object and either the flipped or unflipped object (removing 
its complementary, essentially equal object). 
"""

import random 
import csv
import NovelObject as nObj

def get_stimulus_from_file(file):  
    """Read image filenames from a CSV file.
    :param file: filepath to the CSV file containing more filepaths to stimuli
    :type file: string 
    :rtype file: string list 
    :return stims: list of filepaths to stimuli files
    """
    stims = []
    with open(file, newline='') as stimulus_file:
        stim_file_reader = csv.reader(stimulus_file, delimiter=',')
        for (line_number, text) in enumerate(stim_file_reader):
            if line_number != 0: # ignore the first line (the column name)
                stims.append(text[0]) # fill list with first row
    return stims

def pick_stimuli(uniform, left_oriented, right_oriented):
    """ Selects a random object from the left_oriented or right_oriented lists of 
    NovelObjects, being sure to add their complementary to the other.
    :param uniform: list of uniform NovelObjects
    :type uniform: NovelObjects list
    :param left_oriented: list of uniform NovelObjects that are unflipped
    :type left_oriented: NovelObjects list
    :param right_oriented: list of uniform NovelObjects that are flipped 
    :type right_oriented: NovelObjects list
    :rtype: NovelObject list list 
    :returns: A list of two lists consisting of the novel objects, where each object 
    in either list has a complement in the other and not in the same list 
    """
    orientations = [left_oriented, right_oriented]
    flipped = []
    unflipped = []
    # adds the uniform objects to both lists (they'll always present in both orientations)
    for obj in uniform:
        flipped.append(obj)
        unflipped.append(obj)
    # Choose a random object from some random orientation, and add its complement to 
    # the other orientation list, placing the first in the unflipped list and the second
    # in the flipped list
    while not len(left_oriented) == 0 or not len(right_oriented) == 0:
        orient_choice = random.randint(0, len(orientations) - 1)
        item_choice = random.randint(0, len(orientations[orient_choice]) - 1)
        chosen_item = orientations[orient_choice].pop(item_choice)
        other = orientations[1-orient_choice]
        for (idx, test) in enumerate(other):
            if test.essentially_equal(chosen_item):
                flipped.append(test)
                other.remove(test)
                break
        unflipped.append(chosen_item)
    return [flipped, unflipped]

def setup_experiment(stimulus_list):
    """ Construct and Sorts NovelObjects into whether they are flipped ("right") 
    or unflipped ("left")
    :param stimulus_list: list of stimuli filenames
    :type stimulus_list: string list
    :rtype: NovelObject list list 
    :returns: A list of two lists consisting of the novel objects, where each object 
    in either list has a complement in the other and not in the same list 
    """
    uniform = []
    left = []
    right = []
    all_stimuli = get_stimulus_from_file(stimulus_list)
    for stim in all_stimuli:
        # construct object
        novObj = nObj.NovelObject(stim)
        # sorts the object
        orientation = novObj.get_orientation()
        if orientation == "left":
            left.append(novObj)
        elif orientation == "right":
            right.append(novObj)
        else:
            uniform.append(novObj)
    # returns the randomly chosen stimuli
    if len(left) != len(right):
        return None
    return pick_stimuli(uniform, left, right)
        
class Stimuli:
    """
    This class defines the regimen of stimuli used for the experiment. It does so
    by random picking objects of random orientations.
    """
    def __init__(self, filename):
        """ Constructs a Stimuli (see descriptions above for how such objects
        are defined.)
        :param stimulus_list: filenames
        :type stimulus_list: string 
        """
        self.stimuli = setup_experiment(filename)
        
    def get_stimuli(self):
        """ Return the stimuli
        :rtype: NovelObject list list 
        :returns: A list of two lists consisting of the novel objects, where each object 
        in either list has a complement in the other and not in the same list 
        """
        return self.stimuli
    
    def num_stimuli(self):
        """ Returns the number of stimuli
        :rtype: NovelObject list list 
        :returns: A list of two lists consisting of the novel objects, where each object 
        in either list has a complement in the other and not in the same list 
        """
        if self.stimuli == None:
            return 0
        return len(self.stimuli[0])
      