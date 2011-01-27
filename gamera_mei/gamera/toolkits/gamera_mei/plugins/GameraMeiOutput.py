from gamera.plugin import *
from pymei.Components import MeiDocument
from pymei.Components import Modules as mod

import uuid

# [staff_number, c.offset_x, c.offset_y, note, line_number, 
#   glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows]
#
# [1, 18, 142, '', 3, 'clef', 'c', [''], '', 14, 40]
# [1, 612, 203, 'F', 7, 'neume', 'virga', [''], 'D', 13, 44]

class GameraMeiOutput(object):
    def __init__(self, incoming_data):
        self._recognition_results = incoming_data
        self._meidoc = None
        for ln in self._recognition_results:
            self._parse_line(ln)
        
    def _parse_line(self, line):
        snum, oset_x, oset_y, note, lnum, gkind, glyph, gchar, updown, ncols, nrows = line
        
    
    def _create_zone_element(self, oset_x, oset_y, ncols, nrows):
        zone = mod.zone_()
        zone.id = self._idgen()
        zone.attributes = {'ulx': oset_x, 'uly': oset_y, 'lrx': ncols, 'lry': nrows}
        return zone
    
    def _create_graphic_element(self, imgfile):
        graphic = mod.graphic_()
        graphic.id = self._idgen()
        graphic.attributes = {'xlink:href': imgfile}
        return graphic
    
    def _create_neume_element(self, note, lnum, glyph, updown):
        neume = mod.uneume_()
        neume.id = self._idgen()
        neume.attributes = {'name': glyph}
    
    def _create_note_element(self, note, lnum):
        pass
    
    def _idgen(self):
        """ Returns a UUID. """
        return uuid.uuid4()
    