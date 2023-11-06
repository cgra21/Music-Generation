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

# Decoding process
# 1. NoteEnc -> numpy chord array
# 2. numpy array -> music21.Stream
def npenc2stream(arr, bpm=120):
    "Converts numpy encoding to music21 stream"
    chordarr = npenc2chordarr(np.array(arr)) # 1.
    return chordarr2stream(chordarr, bpm=bpm) # 2.


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
        for elem in part.flatten():
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
    
# The npenc array is Timestep x (note, duration), a dense array
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
    # Note: this is sorted per timestep, so the order is maintained on the overall arr
    if enc_type is None: 
        # note, duration
        return [n[:2] for n in notes] 
    if enc_type == 'parts':
        # note, duration, part
        return [n for n in notes]
    if enc_type == 'full':
        # note_class, duration, octave, instrument
        return [[n%12, d, n//12, i] for n,d,i in notes] 
    

##### DECODING #####

# 1.

# Go from numpy encoding to sparse chordarr
def npenc2chordarr(npenc, note_size=NOTE_SIZE):
    num_instruments = 1 if len(npenc.shape) <= 2 else npenc.max(axis=0)[-1]
    
    max_len = npenc_len(npenc)
    # score_arr = (steps, inst, note)
    score_arr = np.zeros((max_len, num_instruments, note_size))
    
    idx = 0
    # Each step = (timestep, (note, duration))
    for step in npenc:
        n,d,i = (step.tolist()+[0])[:3] # or n,d,i
        if n < VALTSEP: continue # special token
        if n == VALTSEP:
            idx += d
            continue
        score_arr[idx,i,n] = d
    return score_arr

def npenc_len(npenc):
    # for every seperator, add the duration.
    # This will eventually get us the total steps of the array.
    duration = 0
    for t in npenc:
        if t[0] == VALTSEP: duration += t[1]
    return duration + 1


# 2.
# Convert chordarr back to music21.Stream object
def chordarr2stream(arr, sample_freq=SAMPLE_FREQ, bpm=120):

    # Given that our default sample_freq is 4, this is a sixteenth note, or 0.25 of a quarter note
    duration = music21.duration.Duration(1. / sample_freq)
    # Stream subclass for handling music with more than one part
    stream = music21.stream.Score()
    # Adds timesignature to score
    stream.append(music21.meter.TimeSignature(TIMESIG))
    # Sets stream tempo
    stream.append(music21.tempo.MetronomeMark(number=bpm))
    # Adds key signature, input int means number of sharps if positive, or number of flats if negative
    stream.append(music21.key.KeySignature(0))
    # for each instrument
    for inst in range(arr.shape[1]):
        p = partarr2stream(arr[:,inst,:], duration)
        stream.append(p)
    #transpose by number of half steps if input is an int
    stream = stream.transpose(0)
    return stream

# 2b.
def partarr2stream(partarr, duration):
    "convert instrument part to music21 chords"
    part = music21.stream.Part()
    part.append(music21.instrument.Piano())
    part_append_duration_notes(partarr, duration, part) # notes already have duration calculated

    return part

def part_append_duration_notes(partarr, duration, stream):
    "convert instrument part to music21 chords"
    for tidx,t in enumerate(partarr):
        note_idxs = np.where(t > 0)[0] # filter out any negative values (continuous mode) # i.e -1 for seperator, or -2 
        if len(note_idxs) == 0: continue
        notes = []
        for nidx in note_idxs:
            note = music21.note.Note(nidx)
            # For each note, get the duration - which in this case is measured in timesteps, and convert it to a duration in quarternotes
            note.duration = music21.duration.Duration(partarr[tidx,nidx]*duration.quarterLength)
            notes.append(note)
        # for each note grouping
        for g in group_notes_by_duration(notes):
            # if group contains one note:
            if len(g) == 1:
                #tidx - timestep times our duration, which by default is 0.25, this results in the timesteps x 16th note value
                # this gets us the timestep in terms of sixteenth notes
                stream.insert(tidx*duration.quarterLength, g[0])
            else: # there are multiple notes with the same length
                chord = music21.chord.Chord(g) # Create a chord from these notes
                stream.insert(tidx*duration.quarterLength, chord) # insert the chord at the respective 16th note
    return stream


from itertools import groupby
#  combining notes with different durations into a single chord may overwrite conflicting durations. Example: aylictal/still-waters-run-deep
def group_notes_by_duration(notes):
    "separate notes into chord groups"
    # This retrieves the length of a note in relation to quarter notes as a float, ex. 1.0 = quarter note
    # 2.0 = half note
    keyfunc = lambda n: n.duration.quarterLength
    # Sort by note length
    notes = sorted(notes, key=keyfunc)
    # return a list of lists, where each list contains notes with the same duration value
    return [list(g) for k,g in groupby(notes, keyfunc)]


# Midi -> npenc Conversion helpers

# Checks for validity of any given numpy encoding
def is_valid_npenc(npenc, note_range=PIANO_RANGE, max_dur=DUR_SIZE, 
                   min_notes=32, input_path=None, verbose=True):
    if len(npenc) < min_notes:
        if verbose: print('Sequence too short:', len(npenc), input_path)
        return False
    if (npenc[:,1] >= max_dur).any(): 
        if verbose: print(f'npenc exceeds max {max_dur} duration:', npenc[:,1].max(), input_path)
        return False
    # https://en.wikipedia.org/wiki/Scientific_pitch_notation - 88 key range - 21 = A0, 108 = C8
    if ((npenc[...,0] > VALTSEP) & ((npenc[...,0] < note_range[0]) | (npenc[...,0] >= note_range[1]))).any(): 
        print(f'npenc out of piano note range {note_range}:', input_path)
        return False
    return True

# seperates overlapping notes to different tracks
def remove_overlaps(stream, separate_chords=True):
    if not separate_chords:
        #.makeVoices - if there are overlapping notes, put them in different voices
        # .voicesToParts() - self explantory
        return stream.flatten().makeVoices().voicesToParts()
    return separate_melody_chord(stream)

# seperates notes and chords to different tracks
def separate_melody_chord(stream):
    new_stream = music21.stream.Score()
    if stream.timeSignature: new_stream.append(stream.timeSignature)
    # metronomeMarkBoundaries returns offset start, offset end, MetronomeMark for all TempoIndication objects
    # in will return the MetronomeMark for the first TempoIndication
    new_stream.append(stream.metronomeMarkBoundaries()[0][-1])
    if stream.keySignature: new_stream.append(stream.keySignature)
    
    # Collect all individual notes into one part
    melody_part = music21.stream.Part(stream.flatten().getElementsByClass('Note'))
    #insert instrument at timestep 0
    melody_part.insert(0, stream.getInstrument())
    chord_part = music21.stream.Part(stream.flatten().getElementsByClass('Chord'))
    # insert the instrument at timestep 0
    chord_part.insert(0, stream.getInstrument())
    # append both parts to the new stream
    new_stream.append(melody_part)
    new_stream.append(chord_part)
    return new_stream

# processing functions for sanitizing data

def compress_chordarr(chordarr):
    return shorten_chordarr_rests(trim_chordarr_rests(chordarr))

def trim_chordarr_rests(arr, max_rests=4, sample_freq=SAMPLE_FREQ):
    # max rests is in quarter notes
    # max 1 bar between song start and end
    start_idx = 0
    max_sample = max_rests*sample_freq
    for idx,t in enumerate(arr):
        # check if any notes are present, if they are, break the loop
        if (t != 0).any(): break
        # if they aren't, increase the index
        start_idx = idx+1
        
    end_idx = 0
    # Do the same for the end of the array
    for idx,t in enumerate(reversed(arr)):
        if (t != 0).any(): break
        end_idx = idx+1
    
    # get start idx in terms of timesteps
    start_idx = start_idx - start_idx % max_sample
    # get end idx in temrs of timesteps
    end_idx = end_idx - end_idx % max_sample
#     if start_idx > 0 or end_idx > 0: print('Trimming rests. Start, end:', start_idx, len(arr)-end_idx, end_idx)
    return arr[start_idx:(len(arr)-end_idx)]

def shorten_chordarr_rests(arr, max_rests=8, sample_freq=SAMPLE_FREQ):
    # max rests is in quarter notes
    # max 2 bar pause
    rest_count = 0
    result = []
    max_sample = max_rests*sample_freq
    for timestep in arr:
        # if all notes in timestamp are 0, there is a rest
        if (timestep==0).all(): 
            rest_count += 1
        else:
            # check if there is a rest longer than 2 bars
            if rest_count > max_sample:
#                 old_count = rest_count
                rest_count = (rest_count % sample_freq) + max_sample
#                 print(f'Compressing rests: {old_count} -> {rest_count}')
            for i in range(rest_count): result.append(np.zeros(timestep.shape))
            rest_count = 0
            # Add timestep
            result.append(timestep)
    # for remaining rests that aren't greater than 2 bars, append to result
    for i in range(rest_count): result.append(np.zeros(timestep.shape))
    return np.array(result)

# sequence 2 sequence convenience functions

def stream2npenc_parts(stream, sort_pitch=True):
    chordarr = stream2chordarr(stream)
    _,num_parts,_ = chordarr.shape
    # create a list of npenc arrays for each part
    parts = [part_enc(chordarr, i) for i in range(num_parts)]
    # return 
    return sorted(parts, key=avg_pitch, reverse=True) if sort_pitch else parts

def chordarr_combine_parts(parts):
    # Max timestep in the parts
    max_ts = max([p.shape[0] for p in parts])
    # increase part size to max timestep for all parts
    parts_padded = [pad_part_to(p, max_ts) for p in parts]
    chordarr_comb = np.concatenate(parts_padded, axis=1)
    return chordarr_comb

def pad_part_to(p, target_size):
    # Pads rows to end of p to equal max_ts
    pad_width = ((0,target_size-p.shape[0]),(0,0),(0,0))
    return np.pad(p, pad_width, 'constant')

def part_enc(chordarr, part):
    partarr = chordarr[:,part:part+1,:]
    npenc = chordarr2npenc(partarr)
    return npenc

def avg_tempo(t, sep_idx=VALTSEP):
    avg = t[t[:, 0] == sep_idx][:, 1].sum()/t.shape[0]
    avg = int(round(avg/SAMPLE_FREQ))
    return 'mt'+str(min(avg, MTEMPO_SIZE-1))

def avg_pitch(t, sep_idx=VALTSEP):
    # return mean of notes
    return t[t[:, 0] > sep_idx][:, 0].mean()