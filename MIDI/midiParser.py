import mido
import numpy as np

# This will print each track, and their corrisponding messages.
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

# for i in mid.tracks:
#     print(i)


def note_velocity_arr(mid: mido.MidiFile):
    notes = []
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                notes.append([msg.note, msg.velocity])
    return notes

def piano_roll(mid: mido.MidiFile):
    # TODO create piano roll implementation
    # NOTE Will not work with songs of varying tempo
    # Find tempo of track
    for track in mid.tracks:
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
    time_steps = mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo)
    roll = []
    # Need to track previous notes until we get a note_off message, perhaps make a dictionary to track? update dictionary when given a different note activation command
    note_dict = {}
    for i in range(21,89):
        note_dict[i] = 0
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                note_dict[msg.note] == 1
            if msg.type == 'note_off':
                note_dict[msg.note] == 0
    # Need to track time steps in order to fill piano roll properly
    return 

if __name__ == '__main__':
    
    # Read in our midi file
    mid = mido.MidiFile('./mary.mid')
    
    # print(note_velocity_arr(mid))
    # print(mid.length)
    print(mid.ticks_per_beat)
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.is_meta:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
    print(mido.second2tick(mid.length, ticks_per_beat = mid.ticks_per_beat, tempo=tempo))
    test_dict = {}
    for i in range(21,89):
        test_dict[i] = 0
    test_dict[21] = 1
    #print(test_dict)
    test_dict[21] = 1
    #print(test_dict)
    print(list(test_dict.values()))
    test_array = np.zeros((3,88))
    print(test_array)