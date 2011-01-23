from gamera.plugin import *

from pymei.Templates import bare_template
from pymei.Components import MeiDocument
from pymei.Import import parse_mei

import json

class GameraMeiOutput(object):
    def __init__(self, incoming_data=None):
        self._meidoc = None
        self._create_skeleton()
    
    def set_title(self, doctitle):
        """ Sets the document title. """
        pass
    
    def _create_skeleton(self):
        """ 
            Creates a minimal document skeleton to use for the output.
            
            Uses the templates defined in the pymei module for convenience.
            
        """
        self._meidoc = parse_mei(bare_template)