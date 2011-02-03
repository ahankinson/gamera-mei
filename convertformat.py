import cPickle

f = open('glyph_list_sorted.txt')
c = f.readlines()[0].strip()


output = {}

contents = eval(c)

glyph_fields = [
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

old_staff = None

# unique staff numbers.
snums = set([p[0] for p in contents])
for num in snums:
    staff = {}
    if num == '':
        output[None] = {}
        output[None]['content'] = []
    else:
        output[num] = {}
        output[num]['content'] = []
    

for line in contents:
    glyph = dict(zip(glyph_fields, line))
    
    if glyph['gchar'][0] != '':
        glyph['gchar'].insert(0, glyph['gform'])
    else:
        glyph['gchar'][0] = glyph['gform']
    
    
    if glyph['snum'] == '':
        staff_key = None
    else:
        staff_key = glyph['snum']
    
    output[staff_key]['content'].append({
        'type': glyph['gkind'],
        'form': glyph['gchar'],
        'coord': [glyph['oset_x'], glyph['oset_y'], glyph['ncols'], glyph['nrows']],
        'strt_pos': glyph['lnum'],
        'strt_pitch': glyph['note'],
        'direction': glyph['updown']
    })

f = open('datastream.pickle', 'wb')
cPickle.dump(output, f)
f.close()

# check to see if it loads
f = open('datastream.pickle', 'rb')
l = cPickle.load(f)
f.close()
print l
    
    