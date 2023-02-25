import mido

# This will print each track, and their corrisponding messages.
# for i, track in enumerate(mid.tracks):
#     print('Track {}: {}'.format(i, track.name))
#     for msg in track:
#         print(msg)

# for i in mid.tracks:
#     print(i)


def note_velocity_arr(mid: mido.MidiFile):
    notes = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                notes.append([msg.note, msg.velocity])
    return notes


if __name__ == '__main__':
    
# Read in our midi file
    mid = mido.MidiFile('./mary.mid')
    print(note_velocity_arr(mid))