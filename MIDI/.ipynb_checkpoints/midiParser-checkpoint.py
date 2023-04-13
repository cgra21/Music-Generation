
import mido

# This will print each track, and their corrisponding messages.
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

# for i in mid.tracks:
#     print(i)

def to_arr(mid: mido.MidiFile, velocity_based = False, absolute_time = False, binary = False, note_only = False, time_only = False) -> list:
    # This will return a list containing note properties
    # [on/off, note, velocity, deltaTime] for each note
    # TODO: I am just now realizing that you cannot use these kwargs in tandem, this function will break if you try and use them all at once
    # FIX
    if time_only == True:
        times = []
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    times.append(msg.time)
        return times
    if note_only == True:
        notes = []
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    notes.append(msg.note)
        return notes
    if absolute_time == False:
        notes = []
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    notes.append([1, msg.note, msg.velocity, msg.time])
                if msg.type == 'note_off':
                    notes.append([0,msg.note, msg.velocity, msg.time])
    if absolute_time == True:
        abs_time = 0
        notes = []
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    abs_time += msg.time
                    notes.append([1, msg.note, msg.velocity, msg.time, abs_time])
                if msg.type == 'note_off':
                    abs_time += msg.time
                    notes.append([0,msg.note, msg.velocity, msg.time, abs_time])
    if binary == True:
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    abs_time += msg.time
                    notes.append([1, msg.note, msg.time])
                if msg.type == 'note_off':
                    abs_time += msg.time
                    notes.append([0, msg.note, msg.time])
    if velocity_based == True:
        notes = []
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on' and msg.velocity != 0:
                    notes.append(msg.note)
    return notes

def to_duration(notes: list):
    # TODO create two lists, one containing the note, and the other containing the duration of that note
    # Have dictionary of notes that are currently on,  when it is added to dict, start value as 0, as you walk through messages, add deltaTime to all currently on notes, if a note is deactivated, grab its value and duration and append to a list
    pass




def piano_roll(mid: mido.MidiFile):
    # TODO create piano roll implementation
    # TODO This will need to keep track of whether note is on or off, then turn it off at the respective time steps
    # NOTE Will not work with songs of varying tempo



    # Find tempo of track
    for track in mid.tracks:
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo

    #Compute total time steps over entire length of song
    time_steps = int(mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo))
    roll = np.zeros(time_steps,88)
    pass

def msgdict(msg):
    return msg.dict()
    # This will create an empty matrix with time steps * [88] zeros
    # Need to track previous notes until we get a note_off message, perhaps make a dictionary to track? update dictionary when given a different note activation comman
    # Need to track time steps in order to fill piano roll properly

def note_velocity_arr(mid: mido.MidiFile):
    notes = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                notes.append([msg.note, msg.velocity])
    return notes

def to_midi(self, notes, name: str, bpm):
        # TODO Create function to convert back to midi file from array of notes
        tempo = mido.bpm2tempo(bpm)
        new_midi = mido.MidiFile()
        new_track = mido.MidiTrack()
        new_midi.tracks.append(new_track)
        on_status = {1:'note_on',0:'note_off'}
        for note in notes:
            msg = mido.Message(on_status[note[0]], note = note[1], velocity = note[2], time = note[3])
            new_track.append(msg)
        new_midi.save(f'{name}.mid')
        return
    
def note_to_midi(notes: list, name: str):
    '''takes a list of basic notes i.e [65, 55, 34, 28, 64,...] and converts it 
    to a midi file. 
    This midi file will only play one note at a time, at a fixed velocity, and fixed
    timing.'''
    new_midi = mido.MidiFile()
    new_track = mido.MidiTrack()
    for note in notes:
        msg = mido.Message('note_on', note = note, time = 124)
        new_track.append(msg)
        msg_off = mido.Message('note_off',note = note, time = 124)
        new_track.append(msg_off)
    new_midi.tracks.append(new_track)
    new_midi.save(f'{name}.mid')
    return

def time_to_midi(notes, times: list, name: str):
    '''takes a list of midi notes and times and combines them to create
    a new midi file. Must be of same length'''
    if len(notes) != len(times):
        raise Error('lists of unequal length')
    new_midi = mido.MidiFile()
    new_track = mido.MidiTrack()
    for note, time  in zip(notes, times):
        msg = mido.Message('note_on', note = note, time = time)
        new_track.append(msg)
    new_midi.tracks.append(new_track)
    new_midi.save(f'{name}.mid')
    return

if __name__ == '__main__':
    
# Read in our midi file
    mid = mido.MidiFile('./mary.mid')

    
    # print(note_velocity_arr(mid))
    # print(mid.length)
    # print(mid.ticks_per_beat)
    # for i, track in enumerate(mid.tracks):
    #     for msg in track:
    #         if msg.is_meta:
    #             if msg.type == 'set_tempo':
    #                 tempo = msg.tempo
    # print(int(mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo)))
    # test_dict = {}
    # for i in range(21,89):
    #     test_dict[i] = 0
    # test_dict[21] = 1
    # #print(test_dict)
    # test_dict[21] = 1
    #print(test_dict)
    # print(list(test_dict.values()))
    # time_steps = int(mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo))
    # print(np.zeros((time_steps,88))[0])
    #test_array = np.zeros(int(mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo),88))
    #print(test_array)

    # for track in mid.tracks:
    #     for msg in track:
    #         if msg.type == 'note_on':
    #             print(msg.dict())
    notes = to_arr(mid)
    print(to_duration(notes))
