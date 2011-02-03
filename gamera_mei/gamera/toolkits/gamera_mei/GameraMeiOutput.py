from gamera.plugin import *
from gamera.toolkits.gamera_mei.GameraMeiExceptions import *


from pymei.Components import MeiDocument
from pymei.Components import Modules as mod

import logging
lg = logging.getLogger('gm')
f = logging.Formatter("%(levelname)s %(asctime)s On Line: %(lineno)d %(message)s")
h = logging.StreamHandler()
h.setFormatter(f)

lg.setLevel(logging.DEBUG)
lg.addHandler(h)

import uuid
import pdb

# [staff_number, c.offset_x, c.offset_y, note, line_number, 
#   glyph_kind, actual_glyph, glyph_char, uod, c.ncols, c.nrows]
#
# {'direction': 'D', 'form': ['clivis', '2'], 'strt_pos': 5, 'coord': [213, 179, 26, 35], 'strt_pitch': 'A', 'type': 'neume'}, 
# neume.scandicus.flexus.2.q.2.3.dot
# neume.he.torculus.liquescent.2.2
# neume.compound.dot.u3.u2.u2.d2
# neume.torculus.2.2.he.ve


class GameraMeiOutput(object):
    
    # define the form of a neume.
    # form: [ num, interval_dir... ]
    # e.g., clivis: [2, 'd']
    # torculus: [3, 'u', 'd']
    NEUME_NOTES = {
        'punctum': [],
        'virga': [],
        'cephalicus': ['d'],
        'clivis': ['d'],
        'epiphonus': ['u'],
        'podatus': ['u'],
        'porrectus': ['d','u'],
        'scandicus': ['u','u'],
        'torculus': ['u','d'],
        'ancus': ['d','d'], # See note 1 below
    }
    
    # given an alternate form, how many notes does it add to the neume?
    ADD_NOTES = {
        'flexus': ['d'], # scandicus.flexus, porrectus.flexus
        'resupinus': ['u'], # torculus.resupinus
    }
    
    SCALE = ['A','B','C','D','E','F','G']
    
    def __init__(self, incoming_data):
        self._recognition_results = incoming_data
        self.meidoc = mod.mei_()
        self.staff = None
        self.glyph = None
        
        self._note_elements = None
        self._neume_pitches = []
        
        self._global_graphic_element = self._create_graphic_element('foo.jpg')
        self.meidoc.add_child(self._global_graphic_element)
        
        for snum,stf in self._recognition_results.iteritems():
            self.staff = stf
            staffel = self._parse_staff(snum, stf)
            z = mod.zone_()
            z.id = self._idgen()
            z.attributes = {'ulx': self.staff['coord'][0], 'uly': self.staff['coord'][1], \
                                'lrx': self.staff['coord'][2], 'lry': self.staff['coord'][3]}
            
            self._global_graphic_element.add_child(z)
            staffel.facs = z.id
            
            self.meidoc.add_child(staffel)
        
        self.md = MeiDocument.MeiDocument()
        self.md.addelement(self.meidoc)
        
        
    def _parse_staff(self, stfnum, stf):
        staffel = self._create_staff_element()
        staffel.attributes = {'n': stfnum}
        
        for c in self.staff['content']:
            # parse the glyphs per staff.
            self.glyph = c
            
            if c['type'] == 'neume':
                staffel.add_child(self._create_neume_element())
            elif c['type'] == 'clef':
                staffel.add_child(self._create_clef_element())
            elif c['type'] == 'division':
                staffel.add_child(self._create_division_element())
            elif c['type'] == 'custos':
                staffel.add_child(self._create_custos_element())
            elif c['type'] == "alteration":
                staffel.add_child(self._create_alteration_element())
        return staffel
        
    def _create_graphic_element(self, imgfile):
        graphic = mod.graphic_()
        graphic.id = self._idgen()
        graphic.attributes = {'xlink:href': imgfile}
        return graphic
    
    def _create_zone_element(self):
        zone = mod.zone_()
        zone.id = self._idgen()
        zone.attributes = {'ulx': self.glyph['coord'][0], 'uly': self.glyph['coord'][1], \
                            'lrx': self.glyph['coord'][2], 'lry': self.glyph['coord'][3]}
        self._global_graphic_element.add_child(zone)
        return zone
    
    def _create_staff_element(self):
        staff = mod.staff_()
        staff.id = self._idgen()
        return staff
    
    def _create_neume_element(self):
        if 'climacus' in self.glyph['form']:
            neume = mod.ineume_()
        else:
            neume = mod.uneume_()
            
        neume.id = self._idgen()
        zone = self._create_zone_element()
        neume.facs = zone.id
        
        neume.attributes = {'name': self.glyph['form'][0]}
        
        # get the form so we can find the number of notes we need to construct.
        try:
             # since we define the form of the intervals, we're always off-by-one in the number of notes.
            num_notes = len(self.NEUME_NOTES[self.glyph['form'][0]]) + 1
        except KeyError:
            raise GameraMeiFormNotFoundError("The form {0} was not found.".format(self.glyph['form'][0]))
        
        
        # do we need to add any further notes? form is pretty loaded, so we 
        # have to check manually, from idx 1 on (since the primary form is always first)
        
        # we don't have an off-by-one problem here, since an added interval means an added note
        check_additional = [i for i in self.ADD_NOTES.keys() if i in self.glyph['form'][1:]]
        num_notes = num_notes + len(check_additional)
        
        self._neume_pitches = []
        # note elements are everything after the first form. This determines the shape a note takes.
        self._note_elements = self.glyph['form'][1:]
        self._neume_pitches.append(self.glyph['strt_pitch'])
        
        nc = []
        if num_notes > 1:
            # we need to figure out the rest of the pitches in the neume.
            ivals = [int(d) for d in self._note_elements if d.isdigit()]
            try:
                idx = self.SCALE.index(self.glyph['strt_pitch'].upper())
            except ValueError:
                raise GameraMeiPitchNotFoundError("The pitch {0} was not found in the scale".format(self.glyph['strt_pitch']))
                
            if len(ivals) != (num_notes - 1):
                raise GameraMeiNoteIntervalMismatchError("There is a mismatch between the number of notes and number of intervals.")
            
            # note elements = torculus.2.2.he.ve
            # ivals = [2,2]
            # torculus = ['u','d']
            
            lg.debug(ivals)
            for n in xrange(len(ivals)):
                # get the direction
                dir = self.NEUME_NOTES[self.glyph['form'][0]][n]
                lg.debug("direction is {0}".format(dir))
                iv = ivals[n]
                y = idx
                lg.debug("Idx is: {0}".format(y))
                
                lg.debug("Y is: {0}".format(y))
                # since we use "musical counting", a 2 is actually an increase of only
                # one index point, so we only need to progress iv - 1; e.g., an interval
                # of 2 is only one step, so iv = 2 == idx + 1
                for i in xrange(iv - 1):
                    if dir == 'u':
                        lg.debug("going up")
                        y += 1
                        if y > len(self.SCALE):
                            y = 0
                    elif dir == 'd':
                        lg.debug("going down")
                        y -= 1
                        if y < 0:
                            y = len(self.SCALE) - 1
                    # we set idx to y here, since we want to be relative to 
                    # the last note we have, not the starting pitch.
                    idx = y
                    
                lg.debug("Picking pitch {0}".format(self.SCALE[y]))
                self._neume_pitches.append(self.SCALE[y])
        
        for n in xrange(num_notes):
            p = self._neume_pitches[n]
            nc.append(self._create_note_element(p))
        neume.add_children(nc)
        
        lg.debug(neume.children)
        
        return neume
        
    def _create_note_element(self, pname=None):
        note = mod.note_()
        note.id = self._idgen()
        note.pitchname = pname
        return note
    
    def _create_custos_element(self):
        custos = mod.custos_()
        custos.id = self._idgen()
        zone = self._create_zone_element()
        custos.facs = zone.id
        return custos
    
    def _create_clef_element(self):
        clef = mod.clef_()
        clef.id = self._idgen()
        zone = self._create_zone_element()
        clef.facs = zone.id
        return clef
    
    def _create_division_element(self):
        division = mod.division_()
        division.id = self._idgen()
        zone = self._create_zone_element()
        division.facs = zone.id
        return division
    
    def _idgen(self):
        """ Returns a UUID. """
        return str(uuid.uuid4())




if __name__ == "__main__":
    test_data = {
        1: {
            'coord': [1,2,3,4],
            'content': [{
                'type': 'neume',
                'form': ['clivis', '4'],
                'coord': [213, 179, 26, 35],
                'strt_pitch': 'E',
                'strt_pos': 5
            }, {
                'type': 'neume',
                'form': ['torculus', '2', '4'],
                'coord': [213, 179, 26, 35],
                'strt_pitch': 'E',
                'strt_pos': 5
            }]
        }, 2: {
            'coord': [4,5,6,7],
            'content': [{
                'type': '',
                'form': [],
                'coord': [],
                'strt_pitch': 'A',
                'strt_pos': ''
            }]
        }
    }
    
    v = GameraMeiOutput(test_data)
    
    pdb.set_trace()
    
    
    




# [1] http://wwvv.newadvent.org/cathen/10765b.htm; Some of the liquescent 
#   neums have special names. Thus the liquescent podatus is called epiphonus, 
#   the liquescent clivis, cephalicus, the liquescent climacus, ancus.
