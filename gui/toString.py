from piano_roll_grid import PianoRollGrid
from PyQt5.QtWidgets import QGraphicsScene
from music21 import note, chord, stream

class StringConverter:

    def __init__(self, piano_roll_grid):
        self.grid = piano_roll_grid
        self.score = None

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
    
    def convert_to_stream(self):
        s = stream.Stream()
        for start_time, n in self.extract_notes():
            # Set the offset for the note in the stream
            s.insert(start_time, n)
        self.score = s


    # TODO Fix logic? I think it does
    def tokenize(self, score) -> str:
        output = ['xxbos']
        last_offset = 0
        last_duration = 0
        
        # in order to get duration for xxsep token, we need to get offset between currently played note and prev
        for element in score.recurse().stream().notesAndRests:
            if isinstance(element, (note.Note, chord.Chord, note.Rest)):
                if element.offset != last_offset:
                    output.append(f'xxsep d{element.offset - last_offset}')
                    
                if isinstance(element, chord.Chord):
                    # For chords, handle each note in the chord
                    for n in element.notes:
                        midi_pitch = n.pitch.midi
                        dur = n.duration.quarterLength
                        output.append(f'n{midi_pitch} d{dur}')
                        
                elif isinstance(element, note.Note):
                    midi_pitch = element.pitch.midi
                    dur = element.duration.quarterLength
                    output.append(f'n{midi_pitch} d{dur}')
                else:
                    # For rests, just update the duration
                    dur = element.duration.quarterLength
                    output.append(f'n0 d{dur}')
                    
                # Update the last note's offset and duration
                last_offset = element.offset
                last_duration = dur
        
        output.append('xxeos')
        # Join the sequence into a single string
        output_text = ' '.join(output)

        return output
    
    def extract_string(self):
        self.convert_to_stream()
        string = self.tokenize(self.score)
        return string
