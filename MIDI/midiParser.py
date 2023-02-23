import mido
import music21

# This will read in the midi file
mid = mido.MidiFile('mary.mid')

# Iterator through list of tracks in the file
# This also prints their messages
for i in mid.tracks:
    # print(i)
    pass

# This will print all messages for the file
for i in mid:
    # print(i)
    pass

s = music21.converter.parse('mary.mid')
print(s)