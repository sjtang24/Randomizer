"""
NovelObject.py is a module used for anything having to deal with one Novel 
Object. It contains global methods and variables that are very general, as 
well as a class used to create instances of a single NovelObject. 
"""

# CONSTANTS
# These strings are templates for labels necessary to describe the object for 
# the output and for the application.
UNIFORM_LABEL = "Uniform {}"
LHS_LABEL = "{} {}"
RHS_LABEL = "{} {}"

# This dictionary is used to convert colors to its displayable counterparts.
DISPLAY_COLORS = {'Green':'#14c457', 'Red':'red', 'Grey':'white'}

# FUNCTIONS
def split_color(colorname):
    """ Breaks the color into a tuple or string. 
    NOTE: colorname is expected to be of the format "FirstSecond"; it is also
    expected that "First" or "Second" is "Uniform", "Grey", "Green", and "Red" 
    only, where only "First" is "Uniform." If "First" is "Uniform," 
    only "Grey", "Green", and "Red" is returned (as a string). Otherwise, a 
    tuple is returned containing two colors
    
    :param colorname: the color of the novel object
    :type colorname: string
    :rtype colors: string tuple or string
    :return color: string desribing color; or tuple containing colors
    """
    split_len = 0
    # Find second capital letter
    for (char_idx, char) in enumerate(colorname):
        if char_idx > 0 and char.isupper():
            break
        split_len += 1
    # Breaking the string at the capital letter
    colors = (colorname[:split_len], colorname[split_len:])
    if colors[0] == "Uniform":
        return colors[1]
    return colors
    
def get_display_color(color):
    """
    Depending on the color described by the novel object, this method will 
    return a specific color used to display that image stimulus later on.
    :param color: the color that is convertible to a displayable color
    :type color: string
    :rtype: string 
    :return: the displayable version of the color 
    """
    if color in DISPLAY_COLORS.keys():
        return DISPLAY_COLORS[color]
    
# CLASS
class NovelObject:
    """
    This class defines a novel object, and represents the image stimulus itself,
    as well as its labels for when the image is displayed.
    
    NOTE: there is no way to manipulate the attributes of NovelObjects b/c 
    it is informational only.
    """
    def __init__(self, stimuli):
        """
        Constructs a novel object.
        
        It does this by breaking the pathname to the stimuli into multiple parts:
        1) image pathname; 2) colors; 3) ratios; and 4) orientation.
        
        All stimuli filename has the path name "img/X_Y_A.B_Z.JPG" or 
        "img/X_Y.JPG," where X is the "colors," A and B are the "ratios," and 
        Z are the "orientation." 
        
        NOTE: Y the length is always discard and thus unused.
        
        :param colorname: the path to the image the novel object
        :type colorname: string
        """
        unclipped_image = stimuli[4:-4] # remove "img/" and ".JPG" from pathname
        img_info = unclipped_image.split('_')
        img_info.remove('12in') # everything is 12in so remove it 
        if len(img_info) > 1: 
            # will be size 1 if a uniform object
            # writes the ratios in a readable format
            (r1, r2) = tuple(img_info[1].split("."))
            (r1, r2) = (int(r1), int(r2))
            self.ratio = ("{}/{}".format(r1, r2), "{}/{}".format(r2-r1,r2))
            self.orientation = img_info[-1]
        else:
            self.ratio = ()
            self.orientation = ""
        self.colors = split_color(img_info[0])
        self.stimuli = stimuli
    
    def essentially_equal(self, nobj2):
        """ Decides if the instance of NovelObject is the same, where same is
        defined to be the same weight distribution and color.
        :param nobj: the other instance of a NovelObject 
        :type colorname: NovelObject
        :rtype: bool
        :return: whether the two instances are the same
        """
        same_color = self.colors == nobj2.get_colors()
        same_ratio = self.ratio == nobj2.get_ratio()
        return same_color and same_ratio

    def get_stimuli(self):
        """
        Return the pathname to the stimuli
        """
        return self.stimuli
        
    def get_colors(self):
        """
        Returns the color(s) of the stimuli.
        :returns: string desribing the color of a uniform object; or tuple 
        containing the different colors of the stimulus
        """
        return self.colors
        
    def get_ratio(self):
        """
        Returns the ratio(s) of the stimuli.
        :returns: None if the object is uniform; or a tuple containing the 
        ratios of the object
        """
        return self.ratio
        
    def get_orientation(self):
        """
        Returns "left" or "right" depending on the orientation of the novel
        object
        :returns: "left" if the object is flipped, or "right" if it is unflipped
        :rtype: string 
        """
        return self.orientation

    def is_uniform_object(self):
        """
        Returns whether the given object is uniform
        :rtype: bool
        :returns: (see description)
        """
        return type(self.colors) == str
        
    def get_labels(self):
        """
        Returns labels of the different aspects regarding ratio and color of
        the Novel Object.
        :returns labels: (see description)
        :rtype: (string, string) list 
        """
        labels = []
        if self.is_uniform_object():
            labels.append((UNIFORM_LABEL.format(self.colors), self.colors))
        else:
            (c1, c2) = self.colors
            (r1, r2) = self.ratio
            llabel = LHS_LABEL.format(r1, c1)
            rlabel = RHS_LABEL.format(r2, c2)
            labels.append((llabel, c1))
            labels.append((rlabel, c2))
        if self.orientation == "right": # the file name treats essentionally equal objects the same
            labels.reverse()
        return labels
    
    def get_object_info(self): 
        """
        Returns the same information as get_labels but combined them into a 
        single string
        :rtype: string
        :returns combined: information of the ratio of different aspects of the 
        object as one string 
        """
        labels = self.get_labels()
        (fl, c) = labels[0]
        if self.is_uniform_object(): # uniform object
            return fl
        # definitely non-uniform
        (sl, c) = labels[1]
        return fl + " " + sl
