from gamera.plugin import *
from gamera.toolkits.gamera_mei.plugins.GameraMeiExceptions import *


from pymei.Components import MeiDocument
from pymei.Components import Modules as mod

import uuid

# [staff_number, c.offset_x, c.offset_y, note, line_number, 
#   glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows]
#
# [1, 18, 142, '', 3, 'clef', 'c', [''], '', 14, 40]
# [1, 612, 203, 'F', 7, 'neume', 'virga', [''], 'D', 13, 44]

class GameraMeiOutput(object):
    
    # define the number of notes in a neume form.
    NEUME_NOTES = {
        'punctum': 1,
        'virga': 1,
        'ancus': 2, # See note 1 below
        'cephalicus': 2,
        'clivis': 2,
        'epiphonus': 2,
        'podatus': 2,
        'porrectus': 3,
        'salicus': 3,
        'scandicus': 3,
        'torculus': 3,
    }
    
    # given an alternate form, how many notes does it add to the neume?
    ADD_NOTES = {
        'flexus': 1, # scandicus.flexus, porrectus.flexus
        'resupinus': 1, # torculus.resupinus
    }
    
    def __init__(self, incoming_data):
        self._recognition_results = incoming_data
        self._meidoc = None
        
        self.glyph_fields = [
            'snum',
            'oset_x',
            'oset_y',
            'note',
            'lnum',
            'gkind',
            'gform',
            'gchar',
            'updown',
            'ncols',
            'nrows'
        ]
        
        self.glyph = None
        
        for ln in self._recognition_results:
            self._parse_line(ln)
        
    def _parse_line(self, line):
        self.glyph = dict(zip(self.glyph_fields, line))
        
        if self.glyph['gkind'] == "neume":
            self._create_neume_element()
        elif self.glyph['gkind'] == "clef":
            self._create_clef_element()
        elif self.glyph['gkind'] == "custos":
            self._create_custos_element()
        elif self.glyph['gkind'] == "division":
            self._create_division_element()
        elif self.glyph['gkind'] == "alteration":
            self._create_alteration_element()
        
    def _create_graphic_element(self, imgfile):
        graphic = mod.graphic_()
        graphic.id = self._idgen()
        graphic.attributes = {'xlink:href': imgfile}
        return graphic
    
    def _create_zone_element(self):
        zone = mod.zone_()
        zone.id = self._idgen()
        zone.attributes = {'ulx': self.glyph['oset_x'], 'uly': self.glyph['oset_y'], \
                            'lrx': self.glyph['ncols'], 'lry': self.glyph['nrows']}
        return zone
    
    def _create_neume_element(self):
        neume = mod.uneume_()
        neume.id = self._idgen()
        zone = self._create_zone_element()
        neume.attributes = {'name': self.glyph['gform'], 'facs': zone.id}
        
        # get the form so we can find the number of notes we need to construct.
        try:
            num_notes = NEUME_NOTES[self.glyph['gform']]
        except KeyError:
            raise GameraMeiFormNotFoundError("The form {0} was not found.".format(self.glyph['gform']))
        
        # do we need to add any further notes? gchar is pretty loaded, so we 
        # have to check manually.
        check_additional = [i for i in ADD_NOTES.keys() if i in self.glyph['gchar']]
        num_notes = num_notes + ADD_NOTES[check_additional[0]]
        
        nt = []
        for n in xrange(num_notes):
            nt.append(self._create_note_element())
        neume.addchildren(nt)
        
        
    def _create_note_element(self):
        pass
        
    
    def _create_custos_element(self):
        custos = mod.custos_()
        custos.id = self._idgen()
        zone = self._create_zone_element()
        custos.attributes = {'facs': zone.id}
        return custos
    
    def _create_clef_element(self):
        clef = mod.clef_()
        clef.id = self._idgen()
        zone = self._create_zone_element()
        clef.attributes = {'facs': zone.id}
    
    
    def _idgen(self):
        """ Returns a UUID. """
        return uuid.uuid4()






# [1] http://wwvv.newadvent.org/cathen/10765b.htm; Some of the liquescent 
#   neums have special names. Thus the liquescent podatus is called epiphonus, 
#   the liquescent clivis, cephalicus, the liquescent climacus, ancus.
