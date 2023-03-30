
import mido

# This will print each track, and their corrisponding messages.
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

# for i in mid.tracks:
#     print(i)


<<<<<<< HEAD
def to_arr(mid: mido.MidiFile, absolute_time = True, binary = False, note_only = False) -> list:
    # This will return a list containing note properties
    # [on/off, note, velocity, deltaTime] for each note
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
=======
def note_velocity_arr(mid: mido.MidiFile):
    notes = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                notes.append([msg.note, msg.velocity])
    return notes

>>>>>>> parent of f0c16c65 (Update midiParser.py)

if __name__ == '__main__':
    
# Read in our midi file
    mid = mido.MidiFile('./mary.mid')
<<<<<<< HEAD
    
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
=======
    print(note_velocity_arr(mid))
>>>>>>> parent of f0c16c65 (Update midiParser.py)
