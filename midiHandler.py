import music21
import numpy as np

### Music encoding sequence, a lot of code taken from: https://github.com/bearpelican/musicautobot

BPB = 4 # beats per bar
TIMESIG = f'{BPB}/4' # default time signature
PIANO_RANGE = (21, 108)
VALTSEP = -1 # separator value for numpy encoding
VALTCONT = -2 # numpy value for TCONT - needed for compressing chord array

SAMPLE_FREQ = 4 # This is an internal value of midi, it determines how many "timesteps" are included in the file
NOTE_SIZE = 128 # i.e. range of note values
DUR_SIZE = (10*BPB*SAMPLE_FREQ)+1 # Max length - 8 bars. Or 16 beats/quarternotes
MAX_NOTE_DUR = (8*BPB*SAMPLE_FREQ)


##### ENCODING ######

# 1. File To STream

def file2stream(fp):
    # if already a music21 object, return a stream
    if isinstance(fp, music21.midi.MidiFile): return music21.midi.translate.midiFileToStream(fp)
    # Otherwise, parse the file and return a music21 stream
    return music21.converter.parse(fp)


# 2.
def stream2chordarr(s, note_size=NOTE_SIZE, sample_freq=SAMPLE_FREQ, max_note_dur=MAX_NOTE_DUR):

    "Converts music21.Stream to 1-hot numpy array"
    # assuming 4/4 time
    # note x instrument x pitch
    # FYI: midi middle C value=60

    # This will get the highestTime, or that is the last release for the Note and Chord classes.
    # A note has attributes like pitch and duration. Chords can be thought of as a vertical stack of Notes. 
    # Both of these inherit from the GeneralNote class
    highest_time = max(s.flatten().getElementsByClass('Note').highestTime, s.flatten().getElementsByClass('Chord').highestTime)
    #This gets us the max time step in integer format, +1 from the highest time, since highest time is a float
    maxTimeStep = round(highest_time * sample_freq)+1
    # This creates a maxTimeStep x Parts x # of Pitches array
    score_arr = np.zeros((maxTimeStep, len(s.parts), NOTE_SIZE))

    def note_data(pitch, note):
        # This returns a tuple containing the pitch number (0-127), and the offset (measured in quarter notes from the start of the enclosing object), and the 
        # note duration in quarternotes * the sample frequency
        # this effectively returns the pitch number, start and end of each note.
        return (pitch.midi, int(round(note.offset*sample_freq)), int(round(note.duration.quarterLength*sample_freq)))
    
    # iterate through each part and get note and chord information from above
    for idx,part in enumerate(s.parts):
        notes=[]
        for elem in part.flat:
            if isinstance(elem, music21.note.Note):
                notes.append(note_data(elem.pitch, elem))
            if isinstance(elem, music21.chord.Chord):
                for p in elem.pitches:
                    notes.append(note_data(p, elem))

        # sort notes by offset (1), duration (2) so that hits are not overwritten and longer notes have priority
        notes_sorted = sorted(notes, key=lambda x: (x[1], x[2])) 
        for n in notes_sorted:
            if n is None: continue
            pitch,offset,duration = n
            if max_note_dur is not None and duration > max_note_dur: duration = max_note_dur
            score_arr[offset, idx, pitch] = duration
            score_arr[offset+1:offset+duration, idx, pitch] = VALTCONT      # Continue holding note
    return score_arr
    

def chordarr2npenc(chordarr, skip_last_rest=True):
    # combine instruments
    result = []
    wait_count = 0
    for idx,timestep in enumerate(chordarr):
        flat_time = timestep2npenc(timestep)
        if len(flat_time) == 0:
            wait_count += 1
        else:
            # pitch, octave, duration, instrument
            if wait_count > 0: result.append([VALTSEP, wait_count])
            result.extend(flat_time)
            wait_count = 1
    if wait_count > 0 and not skip_last_rest: result.append([VALTSEP, wait_count])
    return np.array(result, dtype=int).reshape(-1, 2) # reshaping. Just in case result is empty

# Note: not worrying about overlaps - as notes will still play. just look tied
# http://web.mit.edu/music21/doc/moduleReference/moduleStream.html#music21.stream.Stream.getOverlaps
def timestep2npenc(timestep, note_range=PIANO_RANGE, enc_type=None):
    # inst x pitch
    notes = []
    for i,n in zip(*timestep.nonzero()):
        d = timestep[i,n]
        if d < 0: continue # only supporting short duration encoding for now
        if n < note_range[0] or n >= note_range[1]: continue # must be within midi range
        notes.append([n,d,i])
        
    notes = sorted(notes, key=lambda x: x[0], reverse=True) # sort by note (highest to lowest)
    
    if enc_type is None: 
        # note, duration
        return [n[:2] for n in notes] 
    if enc_type == 'parts':
        # note, duration, part
        return [n for n in notes]
    if enc_type == 'full':
        # note_class, duration, octave, instrument
        return [[n%12, d, n//12, i] for n,d,i in notes] 