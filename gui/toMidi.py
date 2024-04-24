from music21 import stream, note, midi

class MidiConverter:

    def __init__(self, piano_roll_grid):
        self.grid = piano_roll_grid

    def extract_notes(self):
        notes = []
        for note_button in self.grid.note_buttons:
            start_time = ((note_button.pos().x() + note_button.rect().x()) / self.grid.x_size) - 1  # Calculate start time based on x position
            duration = note_button.dur
            pitch = note_button.noteValue 
            velocity = 64  # Default velocity
            n = note.Note()
            n.pitch.midi = pitch
            n.duration.quarterLength = duration
            n.volume.velocity = velocity
            notes.append((start_time, n))
        return notes
    
    def convert_to_midi(self, filename='output.mid'):
        s = stream.Stream()
        for start_time, n in self.extract_notes():
            # Set the offset for the note in the stream
            s.insert(start_time, n)
        
        mf = midi.translate.streamToMidiFile(s)
        mf.open(filename, 'wb')
        mf.write()
        mf.close()
